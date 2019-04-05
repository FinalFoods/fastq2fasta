from __future__ import print_function
import boto3
from decimal import Decimal
import json
import urllib
import uuid
import datetime
import time
import os

import sys
sys.path.insert(0, './package')
from Bio import SeqIO

s3 = boto3.client('s3')
dynamo_client = boto3.client('dynamodb')

# Get the table name from the Lambda Environment Variable
table_name = os.environ['TABLE_NAME']

# --------------- Main handler ------------------
def lambda_handler(event, context):
    '''
    Uses Rekognition APIs to detect text and labels for objects uploaded to S3
    and store the content in DynamoDB.
    '''
    # Log the the received event locally.
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event.
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    # Log the bucket and key
    print("Input Bucket: " + bucket + " Key: " + key)

    outputBucket = 'iaqportal'

    try:
        # download the FASTQ file to a local file
        localinfile = '/tmp/' + key
        s3.download_file(bucket, key, localinfile)

        # assume local input file is '/tmp/[name].fastq'
        s = localinfile.split('.')
        # define local output file as '/tmp/[name].fasta'
        localoutfile = '.'.join((s[0], 'fasta'))

        # convert file into fasta
        count = SeqIO.convert(localinfile, "fastq", localoutfile, "fasta")
        # Log converted number of records
        print("Converted %i records into fasta" % count)

        # define local output file as '/tmp/[name].qual'
        localoutqualfile = '.'.join((s[0], 'qual'))
        #  convert file into qual
        count = SeqIO.convert(localinfile, "fastq", localoutqualfile, "qual")
        # Log converted number of records
        print("Converted %i records into qual" % count)


        # upload FASTA file to the output bucket
        s3.upload_file(localoutfile, outputBucket,  localoutfile.split('/')[2])

        # upload QUAL file to the output bucket
        s3.upload_file(localoutqualfile, outputBucket,  localoutqualfile.split('/')[2])

        #textDetections = [text['DetectedText'] for text in response['TextDetections']]
        textDetections = "divertiamoci con il textDetections"
        #labels = [{label_prediction['Name']: Decimal(str(label_prediction['Confidence']))} for label_prediction in response['Labels']]
        labels = "ora con le labels"

        # Get the timestamp.
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        # Write to DynamoDB.
        table = boto3.resource('dynamodb').Table(table_name)
        item={'id':key, 'DateTime':timestamp, 'Labels':labels, 'Text':textDetections}
        #table.put_item(Item=item)

        return 'Success'
    except Exception as e:
        print("Error processing object {} from bucket {}. Event {}".format(key, bucket, json.dumps(event, indent=2)))
        raise e
