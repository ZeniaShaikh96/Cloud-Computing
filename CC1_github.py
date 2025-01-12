import boto3

# Step 1: Setting up AWS access credentials

aws_access_key_id = ''
aws_secret_access_key = ''
region = 'us-east-1'
bucket_name = 'cse546-zenia-bucket'


# Step 2: Initializing Boto3 clients for EC2, S3, and SQS

ec2 = boto3.resource('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region) 

s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)

sqs = boto3.resource('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)

# Create an EC2 instance
ami_id = "ami-0182f373e66f89c85"

instance = ec2.create_instances(
    ImageId=ami_id,
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [
            {
                'Key': 'Name',
                'Value': 'App Tier Worker'
            }
        ]
    }]
)

print(f"Created EC2 instance with ID: {instance[0].id}")


# Create S3 bucket
s3.create_bucket(Bucket=bucket_name)

print(f"S3 bucket created. Bucket Name: {bucket_name}")

try:
    s3.create_bucket(Bucket=bucket_name)
    #print("S3 bucket created")
except Exception as e:
    print(f"Error creating bucket: {e}")
    
# Create an SQS client with a specified region
sqs = boto3.client('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)  

# Defining the queue name
queue_name = 'cse-546-zenia-queue'  # Replace with a unique queue name

# Creating the SQS queue
response = sqs.create_queue(QueueName=queue_name)

# Print the Queue URL
print(f"SQS queue created with URL: {response['QueueUrl']}")


import time

# Wait for 1 minute
print("Waiting for 1 minute...")
time.sleep(60)

# List EC2 Instances
ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
response = ec2.describe_instances()
print("Listing all EC2 instances in the current region:")
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")

# List S3 Buckets
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
response = s3.list_buckets()
print("Listing all S3 buckets:")
for bucket in response['Buckets']:
    print(f"Bucket Name: {bucket['Name']}")

# List SQS Queues
sqs = boto3.client('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
response = sqs.list_queues()
if 'QueueUrls' in response:
    print("Listing all SQS queues:")
    for queue_url in response['QueueUrls']:
        print(f"Queue URL: {queue_url}")
else:
    print("No SQS queues found.")
    

# Creating a File and Uploading it to S3
file_name = 'CSE546test.txt'  # Name of the file to be uploaded

# Create an empty file locally
with open(file_name, 'w') as f:
    pass  # This creates an empty file with the name 'CSE546test.txt'

# Upload the file to S3
try:
    s3.upload_file(file_name, bucket_name, file_name)
    print(f"File '{file_name}' uploaded successfully to bucket '{bucket_name}'.")
except Exception as e:
    print(f"Error uploading file: {e}")

import boto3

# Initialize the SQS client
sqs = boto3.client('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)

# Define the SQS queue URL and message details
queue_url = 'https://sqs.us-east-1.amazonaws.com/710271919140/cse-546-zenia-queue'  # Replace with your SQS queue URL
message_body = "This is a test message"  # The actual content of the message
message_name = "test message"  # A name you can use for identification

# Send the message to the SQS queue
response = sqs.send_message(
    QueueUrl=queue_url,  # The SQS queue URL
    MessageBody=message_body,  # The actual message body content
    MessageAttributes={
        'MessageName': {
            'StringValue': message_name,
            'DataType': 'String'
        }
    }
)

# Print the response from AWS
print(f"Message sent! Message ID: {response['MessageId']}")

# Initialize the SQS client
sqs = boto3.client('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)

# Define the SQS queue URL
queue_url = 'https://sqs.us-east-1.amazonaws.com/710271919140/cse-546-zenia-queue'  # Replace with your SQS queue URL

# Get queue attributes including the number of messages
response = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=['ApproximateNumberOfMessages']
)
time.sleep(20)
# Extract the number of messages from the response
message_count = response['Attributes']['ApproximateNumberOfMessages']

# Print the number of messages in the queue
print(f"Number of messages in the queue: {message_count}")

# Initialize the SQS client
sqs = boto3.client('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)

# Define the SQS queue URL
queue_url = 'https://sqs.us-east-1.amazonaws.com/710271919140/cse-546-zenia-queue' 

# Receive the message from the queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1,  # We only need to pull one message
    MessageAttributeNames=['All'],  # This will retrieve all message attributes
    
)

# Extract the message body and attributes
if 'Messages' in response:
    message = response['Messages'][0]  # The message received
    message_body = message['Body']  # Message body content
    message_attributes = message.get('MessageAttributes', {})  # Extract message attributes

    # Extract the message title (if it exists) from the attributes
    message_title = message_attributes.get('MessageName', {}).get('StringValue', 'No Title')

    # Print the message title and body
    print(f"Message Title: {message_title}")
    print(f"Message Body: {message_body}")


# Check the number of messages in the queue before waiting
response_before_wait = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=['ApproximateNumberOfMessages']
)

# Get the number of messages
num_messages_before = response_before_wait['Attributes']['ApproximateNumberOfMessages']
print(f"Number of messages in the queue before waiting: {num_messages_before}")

# Wait for 10 seconds
time.sleep(10)

# Check the number of messages in the queue after waiting
response_after_wait = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=['ApproximateNumberOfMessages']
)

# Get the number of messages
num_messages_after = response_after_wait['Attributes']['ApproximateNumberOfMessages']
print(f"Number of messages in the queue after waiting: {num_messages_after}")

# Initialize Boto3 clients for EC2, S3, and SQS
ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
sqs_client = boto3.client('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)

# Delete all EC2 instances
def delete_ec2_instances():
    instances = ec2_client.describe_instances()
    instance_ids = []
    
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    
    if instance_ids:
        ec2_client.terminate_instances(InstanceIds=instance_ids)
        print(f"Terminated EC2 instances: {instance_ids}")
    else:
        print("No EC2 instances found to terminate.")

# Delete all S3 buckets
def delete_s3_buckets():
    buckets = s3_client.list_buckets()
    bucket_names = []

    for bucket in buckets['Buckets']:
        bucket_names.append(bucket['Name'])

    for bucket_name in bucket_names:
        # Delete all objects in the bucket
        objects = s3_client.list_objects(Bucket=bucket_name)
        if 'Contents' in objects:
            s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': [{'Key': obj['Key']} for obj in objects['Contents']]})
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"Deleted S3 bucket: {bucket_name}")

# Delete all SQS queues
def delete_sqs_queues():
    queues = sqs_client.list_queues()
    
    if 'QueueUrls' in queues:
        for queue_url in queues['QueueUrls']:
            sqs_client.delete_queue(QueueUrl=queue_url)
            print(f"Deleted SQS queue: {queue_url}")
    else:
        print("No SQS queues found to delete.")

# Call the delete functions
delete_ec2_instances()
delete_s3_buckets()
delete_sqs_queues()

# Wait for 20 seconds
print("Waiting for 20 seconds...")
time.sleep(20)
print("Deletion process completed.")

# Initialize Boto3 clients for EC2, S3, and SQS
ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
sqs_client = boto3.client('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)

# List EC2 instances
def list_ec2_instances():
    response = ec2_client.describe_instances()
    instances = []
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'InstanceId': instance['InstanceId'],
                'State': instance['State']['Name'],
                'InstanceType': instance['InstanceType'],
                'PublicIpAddress': instance.get('PublicIpAddress', 'N/A')
            })
    
    return instances

# List S3 buckets
def list_s3_buckets():
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return buckets

# List SQS queues
def list_sqs_queues():
    response = sqs_client.list_queues()
    queues = response.get('QueueUrls', [])
    return queues

# Call the functions and print results
if __name__ == "__main__":
    print("Listing EC2 Instances:")
    ec2_instances = list_ec2_instances()
    if ec2_instances:
        for instance in ec2_instances:
            print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']}, Type: {instance['InstanceType']}, Public IP: {instance['PublicIpAddress']}")
    else:
        print("No EC2 instances found.")

    print("\nListing S3 Buckets:")
    s3_buckets = list_s3_buckets()
    if s3_buckets:
        for bucket in s3_buckets:
            print(f"Bucket Name: {bucket}")
    else:
        print("No S3 buckets found.")

    print("\nListing SQS Queues:")
    sqs_queues = list_sqs_queues()
    if sqs_queues:
        for queue in sqs_queues:
            print(f"Empty Queue with URL: {queue}")
    else:
        print("No SQS queues found.")


