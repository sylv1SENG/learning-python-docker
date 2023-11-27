import os #ouvrir des ficheirs sur l'ordi
import boto3 #client python pour se connecter à la base de dd

s3 = boto3.resource('s3',
                    endpoint_url='http://localhost:9000',
                    aws_access_key_id='admin',
                    aws_secret_access_key='adminadmin')

s3.Bucket('dossiertest1').upload_file('/Users/sylvainsengbandith/Desktop/python_simon2/file3.csv','log1.csv')










#info docker compose 

#version: '3'
#services:
#  minio:
#    image: minio/minio
#    ports:
#      - "38853:38853"
#      - "9000:9000" 
#    environment:
#      MINIO_ACCESS_KEY: coucoujetest123
#      MINIO_SECRET_KEY: cestmakeysecrete123
#      MINIO_CONSOLE_ADDRESS: :38853
#      MINIO_ROOT_USER: admin
#      MINIO_ROOT_PASSWORD: adminadmin
#    command: server /data
#    volumes:
#      - ./resources:/data
