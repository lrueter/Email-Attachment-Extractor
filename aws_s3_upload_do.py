import logging
import boto3
from botocore.exceptions import ClientError
import os
import sys
import threading
 

# Get environment variables
#AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
#AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, Callback=ProgressPercentage(file_name))
    except ClientError as e:
        logging.error(e)
        return False
    return True

def main():

    #TODO change path
    file = "./Inbox-001.mbox"
    bucket = "gmail-export-bucket-1d7b61a8-7e8b-11ed-a1eb-0242ac120002"
    key = "Inbox-001.mbox"

    upload_file(file, bucket, key)

if __name__ == '__main__':
    main()

