import boto3
from django.conf import settings
from botocore.exceptions import ClientError

class S3Service:
    @staticmethod
    def generate_presigned_url(file_name, file_type):
        try:
            # Initialize S3 client using boto3
            s3_client = boto3.client(
                's3',
                region_name=settings.AWS_S3_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            # Generate the pre-signed URL
            presigned_url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': file_name,  # Use file_name from request
                    'ContentType': file_type  # Use file_type from request
                },
                ExpiresIn=settings.AWS_S3_FILE_EXPIRE
            )

            return presigned_url
        except ClientError as e:
            raise Exception(f"Failed to generate pre-signed URL: {str(e)}")

