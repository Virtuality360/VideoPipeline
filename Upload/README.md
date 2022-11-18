# Installing
Use the provided v2pSetup.sh script to install the dependencies for this tool.

# To Run
You will need to add/change a .env file in the same directory as  upload.py to hold the s3 credentials
Use the Minio credentials and the v360psql credentials

AWS_ACCESS_KEY_ID={S3_username}\
AWS_SECRET_ACCESS_KEY={S3_password}\
PGUSER={database_username}\
PGPASSWORD={database_password}\
PGDATABSE=v360psql\
PGHOST=db1.server.internal\
PGPORT=5432

1) Navigate to the folder with the .mp4 videos in the terminal
2) Run upload.py via the terminal
3) Follow the on screen prompts

Three questions will be asked of you, 
- The country the videos were taken in
- The city/region of that country
- What project this is for
- The framerate wanted

The database will be queried to see if the project already exists,
if it does not the program asks you to double check your input for any typos.
If the information is correct, you can continue.

You will then be given two lists, one of videos with the GPMF data, and on without.
Only videos that have the GPMF data will be uploaded to the bucket.

