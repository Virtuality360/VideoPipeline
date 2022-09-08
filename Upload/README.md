# Installing
MediaInfo is required for this program to run properly.
If you get an error asking you to install media-info, you can do so by
installing via https://mediaarea.net/en/MediaInfo (any device) or with brew install media-info (Macs only)

# To Run
You will need to add a .env file with upload .py that holds credentials
AWS_ACCESS_KEY_ID={S3_username}
AWS_SECRET_ACCESS_KEY={S3_password}
PGUSER={database_username}
PGPASSWORD={database_password}
PGDATABSE={database}
PGHOST={database_url}
PGPORT={database_port}

Move upload.py to the folder that contains the *.mp4 videos
Run python3 upload.py or just ./upload.py

Three questions will be asked of you, 
- The country the videos were taken in
- The city/region of that country
- and what project this is for

The database will be queried to see if the project already exists,
if it does not the program asks you to double check your input for any typos.
If the information is correct, you can cantinue

Then you will be given two lists, one of videos with the GPMF data, and on without.
Only videos that have the GPMF data will be uploaded to the bucket

