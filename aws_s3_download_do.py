import boto3
import os

# Get environment variables
#AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
#AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

def main():

    #TODO change path
    file = "./outputV3.zip"
    bucket = "gmail-export-bucket-1d7b61a8-7e8b-11ed-a1eb-0242ac120002"
    key = "MBOX_pdf_outputV2.zip"

    s3 = boto3.client('s3')
    s3.download_file(bucket, key, file)

if __name__ == '__main__':
    main()
