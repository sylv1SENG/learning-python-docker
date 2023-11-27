# learning-python-docker

This project is about to learn how to manipulate different services and how each service is connecting to each other. 
It is about manipulating differents topics and to discover : dockers and python

What is the project : 

- Being able to create a python script which is connecting to an API and retrieve some data 
- Being able to use Docker in order to : 
-> Create a data warehouse and send the retrieve that we retrieve to go there 
->  Connect the data warehouse and connect to a data lake in order to process the data there 
-> Connect the data lake to a data viz tools to display graph 

Resources : 
Make sure your computer will be able to handle Docker 
Make sure your computer is update for Docker and Anaconda 
Make sure you have an API access : here the project is to manipulate a specific data from SEOLyzer

Setup :  


1. Install Docker 
For that, you have to go to Docker website and download the latest version of Docker 


2. Minio : our data warehouse 

Install Minio 

From your terminal on MAC : 

  docker run -p 38853:38853 \
  -e MINIO_ACCESS_KEY="coucoujetest123" \
  -e MINIO_SECRET_KEY="cestmakeysecrete123" \
  -e MINIO_CONSOLE_ADDRESS=:38853 \
  -v /Users/sylvain/Desktop/data-minio:/data \
  minio/minio server /data

NB : 
// Console_address : indicate where the port web to access on your local machine 
// -p 38853:38853 : indicate where is the different container web and API 


From Docker compose file : 

version: '3'
services:
  minio:
    image: minio/minio
    container_name: minio
    ports:
      - "38853:38853" #Desktop
      - "9000:9000"  #API
    environment:
      MINIO_ACCESS_KEY: coucoujetest123
      MINIO_SECRET_KEY: cestmakeysecrete123
      MINIO_CONSOLE_ADDRESS: :38853
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: adminadmin
    command: server /data
    volumes:
      - ./resources:/data


NB : 
// Volumes : Specifies where you want to stock the data in your local machine 
// Command : Specifies the command to run inside the container, starting the Minio server and using /data as the data directory. 


3. Clickhouse and Metabase 

Important to add driver between Clickhouse and Métabase 
Download and install drivers on resources folder 


4. Metabase configuration

Some terminal command 

docker exec -it clickhouse clickhouse-client -u myuser --password mypassword : to connect to clickhouse interface in order to do query 


5. Python File 

Step1 : extract_seolizer_logs() : he is connecting and extracting the data
Step 2 : get_seolizer_log_records_headers(data=data, custom_fields=["Verif_statut"]) : he is getting the header and will add another “heading” from a personnalize need 
Step 3 : transform_seolizer_log_records : he is creating the new table and adding new value from the data we extract early 
Step 4 : write_data_to_local_json : he is writing the data to a local file that we can upload later on the data warehouse 

6. Send data minio to clickhouse 

Run the script : upload_file_to_minio.py 

7. Run docker compose file 

8 : Connect to Metabase in localhost 

Enjoy your graph 


 

