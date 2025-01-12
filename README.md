## AWS Project Steps

### AWS Setup:
- Ensure you have AWS credentials (Access Key ID, Secret Access Key) configured in your environment to access AWS services.
- The credentials can be obtained through the AWS console and configured in your local environment.

## Summary of Required Libraries:
- **Boto3**: For AWS API interactions using command Line - pip install boto3
- **Time**: For delays and resource management timing.

### Resource Creation:
1. Request an EC2 instance (Ubuntu `t2.micro`) using your key pair with your name.
2. Create an S3 bucket.
3. Create an SQS queue (FIFO type).

### Perform the Following Actions:
1. Wait for 1 minute after resource creation.
2. List all active EC2 instances, S3 buckets, and SQS queues in the region.
3. Upload a file named `CSE546test.txt` to the S3 bucket.
4. Send a message with the title "test message" and body "This is a test message" to the SQS queue.
5. Check and print the number of messages in the SQS queue.
6. Retrieve and print the message sent to the SQS queue.
7. Re-check and print the number of messages left in the queue.
8. Wait for 10 seconds before deleting the resources.

### Resource Deletion:
1. Delete the EC2 instance, S3 bucket, and SQS queue.
2. Wait for 20 seconds and list all remaining EC2 instances, S3 buckets, and SQS queues to verify deletion.

### Logging:
- Print a message for each action, such as:
  - "Request sent, wait for 1 min."
  - "Message sent."
  - And others as appropriate.

## Prerequisites
- AWS account with access to create EC2, S3, and SQS resources.
- Access to your AWS credentials (Access Key ID and Secret Access Key).
- AWS SDK installed (e.g., Boto3 for Python, AWS SDK for JavaScript, etc.).
- Basic understanding of AWS services (EC2, S3, and SQS).


-----------------------------------------------------------------------------------------------------------------------------------------

Terminal Output:
PS C:\Users\shaik> & C:/Users/shaik/AppData/Local/Programs/Python/Python312/python.exe c:/Users/shaik/.vscode/extensions/sourcery.sourcery-1.22.0/CC1.py
Created EC2 instance with ID: i-0aa5ac3c6d8538e46
S3 bucket created. Bucket Name: cse546-zenia-bucket
SQS queue created with URL: https://sqs.us-east-1.amazonaws.com/710271919140/cse-546-zenia-queue
Waiting for 1 minute...
Listing all EC2 instances in the current region:
Instance ID: i-0aa5ac3c6d8538e46, State: running
Bucket Name: cse546-zenia-bucket
Listing all SQS queues:
Queue URL: https://sqs.us-east-1.amazonaws.com/710271919140/cse-546-zenia-queue
File 'CSE546test.txt' uploaded successfully to bucket 'cse546-zenia-bucket'.
Message sent! Message ID: 730b054f-db7b-4e99-9d66-7b1d38f6c02d
Number of messages in the queue: 1
Number of messages in the queue before waiting: 0
Number of messages in the queue after waiting: 0
Terminated EC2 instances: ['i-0aa5ac3c6d8538e46']
Deleted S3 bucket: cse546-zenia-bucket
Deleted SQS queue: https://sqs.us-east-1.amazonaws.com/710271919140/cse-546-zenia-queue
Waiting for 20 seconds...
Deletion process completed.
Listing EC2 Instances:
Instance ID: i-0aa5ac3c6d8538e46, State: shutting-down, Type: t2.micro, Public IP: 54.210.215.171

Listing S3 Buckets:
No S3 buckets found.

Listing SQS Queues:
Empty Queue with URL: https://sqs.us-east-1.amazonaws.com/710271919140/cse-546-zenia-queue
PS C:\Users\shaik>

