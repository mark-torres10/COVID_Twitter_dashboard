"""

    aws_helpers.py

    Series of helper functions for working with AWS

"""
import boto3


def save_to_AWS(local_file, s3_file, AWS_resource, AWS_bucket, AWS_access, AWS_secret):
    """

    Saves a local file to AWS

    Args:
        local_file: path (str) to a local file to export to AWS
        s3_file: path (str) of file within the S3 bucket
        AWS_resource: the AWS resource used (e.g., "s3", "ec2", "dynamodb")
        AWS_bucket: name of S3 bucket
        AWS_access: AWS access key
        AWS_secret: AWS secret key

    """

    # connect boto3 wih AWS
    try:
        s3 = boto3.client(AWS_resource,
                          aws_access_key_id=AWS_access,
                          aws_secret_access_key=AWS_secret)
    except Exception as e:
        print("Connection with AWS unsuccessful")
        print(e)
        raise ValueError("Please fix connection error to AWS resource")

    # upload data to AWS
    try:
        s3.upload_file(local_file, AWS_bucket, s3_file)
    except Exception as e:
        print("Error in uploading data to AWS")
        print(e)
        raise ValueError("Please fix error in uploading data to AWS")
    finally:
        return None


def load_from_AWS(local_file, s3_file, AWS_resource, AWS_bucket, AWS_access, AWS_secret):
    """

    Loads a file from an AWS resource (likely to be 's3')

    Args:
        local_file: path (str) to a local file to export to AWS
        s3_file: path (str) of file within the S3 bucket
        AWS_resource: the AWS resource used (e.g., "s3", "ec2", "dynamodb")
        AWS_bucket: name of S3 bucket
        AWS_access: AWS access key
        AWS_secret: AWS secret key
    """
    # connect boto3 wih AWS
    try:
        s3 = boto3.client(AWS_resource,
                          aws_access_key_id=AWS_access,
                          aws_secret_access_key=AWS_secret)
    except Exception as e:
        print("Connection with AWS unsuccessful")
        print(e)
        raise ValueError("Please fix connection error to AWS resource")

    try:
        s3.download_file(Bucket=AWS_bucket, Key=s3_file, Filename=local_file)

    except Exception as e:
        print("Unable to download file from AWS to local storage")
        print(e)
        raise ValueError("Please fix error")

    finally:
        return None
