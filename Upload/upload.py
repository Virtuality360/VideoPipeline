#!/usr/bin/env python3

# Required for file handling
import os.path
# Required for connecting to the s3 bucket
import boto3
# Required for querying the database
import psycopg2
# Required for checking for metadata tracks
from pymediainfo import MediaInfo
# Helps genenerate a unique filename
import datetime
import time
import uuid
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

def load_files():
    """
    Loads all *.mp4 files in the current directory
    Returns two lists, one with mp4s containing telemetry information
    and one with videos that don't have telemetry
    """
    dir = '.'
    allfiles = os.listdir(dir)

    mp4files = [fname for fname in allfiles if fname.endswith(".mp4")]
    valid_mp4 = []

    for file in mp4files:
        try:
            tracks = MediaInfo.parse(file).tracks
        except:
            print(colored_text("Please install media-info, https://mediaarea.net/en/MediaInfo or brew install media-info", "error"))
            exit(-1)
        # There should be four tracks
        # 0:0 - General - Metadata
        # 0:1 - Video
        # 0:2 - Audio
        # 0:3 - Other - GoPro Telemetry
        for track in tracks:
            if track.track_type == "General":
                # Go from UTC timestamp to unix time, convert to int then string to remove trailing .0
                unix_time = str(int(time.mktime(datetime.datetime.strptime(track.encoded_date, "UTC %Y-%m-%d %H:%M:%S").timetuple())))
            if track.track_type == "Other" and track.type == "meta":
                valid_mp4.append([file, unix_time])
                mp4files.remove(file)
    
    return (valid_mp4, mp4files)

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

def upload_to_s3(files, country, city, project):
    """
    Uploads all files in the files list to a s3 bucket
    under the object country/city/project
    """

    S3_HOST_URL = "http://localhost:9000"

    s3_client = boto3.client('s3',
        endpoint_url=S3_HOST_URL,
        config=boto3.session.Config(signature_version='s3v4')
    )
    
    bucket = "v360video"

    for file in files:
        filename = str(uuid.uuid4()) + "_" + file[1] + ".mp4"
        try:
            obj = f"{country}/{city}/{project}/{filename}"
            s3_client.upload_file(file[0], bucket, obj)
        except Exception as e:
            print(colored_text(e, "error"))

def main():
    """
    Function to run when this file is run as a script
    """
    country = input(colored_text("What country are we working on? ")).upper()
    city = input(colored_text("What city are we in? ")).upper()
    project = input(colored_text("And what is the project name/number? ")).upper()

    if not does_project_exist_on_db(country, city, project):
        ans = input(colored_text(f"{country}/{city}/{project} does not currently exist. Continue anyways? (Y/N) ", "warning")).upper()
        if(ans == "N"):
            exit(-1)

    valid_files, invalid_files = load_files()


    print(colored_text(f"The files: {', '.join([item[0] for item in valid_files])} will be uploaded to the minio bucket v360videos/{country}/{city}/{project}."))
    print(colored_text(f"{invalid_files} will not be uploaded - they have no gpmf track.", "warning"))
    ans = input(colored_text(f"Proceed (Y/N)? ")).upper()

    if ans != 'Y':
        print(colored_text("Exiting process"))
        exit()

    upload_to_s3(valid_files, country, city, project)

if __name__ == "__main__":
    main()