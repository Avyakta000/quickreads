
import boto3
from django.conf import settings
from botocore.exceptions import ClientError

class S3Service:
    @staticmethod
    def generate_presigned_url(file_name, file_type):
        try:
            # Initialize S3 client
            s3_client = boto3.client(
                's3',
                region_name=settings.AWS_S3_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            # default directory for file uploads
            directory = 'quicklit_uploads' 
            
            # the full path (Key) for the file
            file_key = f"{directory}/{file_name}"

            # Generate the pre-signed URL for uploading
            presigned_url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': file_key, 
                    'ContentType': file_type
                },
                ExpiresIn=settings.AWS_S3_FILE_EXPIRE
            )

            return presigned_url
        except ClientError as e:
            raise Exception(f"Failed to generate pre-signed URL for upload: {str(e)}")

    @staticmethod
    def delete_file_from_s3(file_name):
        try:
            # Initialize S3 client
            s3_client = boto3.client(
                's3',
                region_name=settings.AWS_S3_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

           # Delete the file from S3
            s3_client.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_name
            )

            return True # return on successful deletion

        except ClientError as e:
            raise Exception(f"Failed to delete file: {str(e)}")

# import boto3
# from django.conf import settings
# from botocore.exceptions import ClientError

# class S3Service:
#     @staticmethod
#     def generate_presigned_url(file_name, file_type):
#         try:
#             # Initialize S3 client using boto3
#             s3_client = boto3.client(
#                 's3',
#                 region_name=settings.AWS_S3_REGION_NAME,
#                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
#             )

#             # Generate the pre-signed URL
#             presigned_url = s3_client.generate_presigned_url(
#                 'put_object',
#                 Params={
#                     'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
#                     'Key': file_name,  # Use file_name from request
#                     'ContentType': file_type  # Use file_type from request
#                 },
#                 ExpiresIn=settings.AWS_S3_FILE_EXPIRE
#             )

#             return presigned_url
#         except ClientError as e:
#             raise Exception(f"Failed to generate pre-signed URL: {str(e)}")

