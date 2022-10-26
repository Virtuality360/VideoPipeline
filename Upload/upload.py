#!/usr/bin/env python3

# Required for file handling
import os.path
import json
# Required for connecting to the s3 bucket
import boto3
import pika
# Required for checking for metadata tracks
from pymediainfo import MediaInfo
# Helps genenerate a unique filename
import datetime
import time
import zlib
# Required for the spinner
from halo import Halo
# Required to load the connection credentials
from dotenv import load_dotenv
# Tries to import psycopg3 if available, otherwise falls back to psycopg2
try:
    import psycopg3
except:
    import psycopg2 as psycopg

# Loads the enviroment varaible to get the connection secrets
load_dotenv()

def colored_text(text, type = "normal"):
    """
    Takes a string and adds color to it based on its type
    Colors are derived from ANSI escape codes
    May not work on all terminals
    normal -> white
    warning -> yellow
    error -> red
    reset -> should reset to default, doesn't seem to work: goes to white.
    """
    class TERM_COLORS:
        WHITE = "\u001b[38;5;231m"
        WARNING = "\033[93m"
        ERROR = "\033[91m"
        RESET = "\u001b[0m"

    match type.lower():
        case "normal":
            color = TERM_COLORS.WHITE
        case "warning":
            color = TERM_COLORS.WARNING
        case "error":
            color = TERM_COLORS.ERROR
        case _:
            color = ""
    return f"{color}{text}{TERM_COLORS.RESET}"

def amqp_conn():
    amqp_host = "prodportainer1.server.internal"
    amqp_port = 5672
    ampq_credentials = pika.PlainCredentials("admin", "password")  # Username, Password

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=amqp_host, port=amqp_port, credentials=ampq_credentials
        )
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="bucketevents", exchange_type="topic")

    return channel

def load_files():
    """
    Loads all *.mp4 files in the current directory
    Returns two lists, one with mp4s containing telemetry information
    and one with videos that don't have telemetry
    """
    dir = '.'
    allfiles = os.listdir(dir)

    mp4files = [fname for fname in allfiles if fname.endswith(".mp4")]
    valid_mp4, invalid_mp4 = [], []

    for file in mp4files:
        try:
            other_track = MediaInfo.parse(file).other_tracks[0]
            # if the duration of the other track (GPMF) is less than one second
            # it is probably empty -> created during the 360 to mp4 process
            # usually around 400 ms - 1000 to be safe
            if other_track.duration < 1000:
                invalid_mp4.append(file)
            else:
                date_raw = (MediaInfo.parse(file).general_tracks[0].encoded_date)
                date_obj = datetime.datetime.strptime(date_raw, "UTC %Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
                #unix_time = str(int(time.mktime(datetime.datetime.strptime(encode_date, "UTC %Y-%m-%d %H:%M:%S").timetuple())))
                valid_mp4.append([date_obj, file])
        except:
            invalid_mp4.append(file)

    return (valid_mp4, invalid_mp4)

def crc32(filename, chunksize=65536):
    """Compute the CRC-32 checksum of the contents of the given filename"""
    with open(filename, "rb") as f:
        checksum = 0
        while (chunk := f.read(chunksize)) :
            checksum = zlib.crc32(chunk, checksum)
        return checksum

@Halo(text='Checking if project exists', spinner='dots')
def does_project_exist_on_db(country, city, project):
    """
    Connects to a database and returns true if the inputs can be found
    """
    with psycopg.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""select from public.v360_exif_data where 
                        country=%s and city=%s and project=%s
                        LIMIT 1""", (country, city, project))
            if(cur.fetchone() == None):
                return False
            else:
                return True

def upload_to_s3(files, country, city, project, fps, priority):
    """
    Uploads all files in the files list to a s3 bucket
    under the object country/city/project
    Videos are uploaded with the naming scheme: {crc32}_{timestamp}.mp4
    """

    S3_HOST_URL = "http://storage3.server.internal:9000"

    s3_client = boto3.client('s3',
        endpoint_url=S3_HOST_URL,
        config=boto3.session.Config(signature_version='s3v4')
    )
    channel = amqp_conn()

    bucket = "v360mp4-upload"

    for file in files:
        filename = f"{file[0]}_{crc32(file[1]):x}.mp4"
        try:
            obj = f"{country}/{city}/{project}/{filename}"
            s3_client.upload_file(file[0], bucket, obj)
            msg_body = json.dumps({"bucket": bucket, "path": f"/{country}/{city}/{project}/", "filename": filename, "fps": fps, "priority": priority})
            amqp_conn().basic_publish(exchange="videoPipeline", routing_key="initialUpload", body=str(msg_body), properties=pika.BasicProperties(priority=priority))
        except Exception as e:
            print(colored_text(e, "error"))
    channel.close()

def main():
    """
    Function to run when this file is run as a script
    """
    country = input(colored_text("What country are we working on? ")).upper()
    city = input(colored_text("What city are we in? ")).upper()
    project = input(colored_text("And what is the project name/number? ")).upper()
    
    if not does_project_exist_on_db(country, city, project):
        ans = input(colored_text(f"{country}/{city}/{project} does not currently exist. Continue anyways? (Y/N) ", "warning")).upper()
        if(ans != "Y"):
            exit(-1)

    fps = float(input(colored_text("How many frames per second? ")))
    priority = int(input(colored_text("Is this low(0), medium(1), or high priority(2)? Enter the number. ")))

    valid_files, invalid_files = load_files()

    print(colored_text(f"The file(s): {', '.join([item[1] for item in valid_files])} will be uploaded to the minio bucket v360videos/{country}/{city}/{project}."))
    print(colored_text(f"The file(s): {', '.join([item for item in invalid_files])} will not be uploaded - the GPMF track is less than 1 second long.", "warning"))
    ans = input(colored_text(f"Proceed (Y/N)? ")).upper()

    if ans != 'Y':
        print(colored_text("Exiting process"))
        exit()

    upload_to_s3(valid_files, country, city, project, fps, priority)

if __name__ == "__main__":
    main()