from storages.backends.s3boto3 import S3Boto3Storage


# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static')
MediaRootS3BotoStorage  = lambda: S3Boto3Storage(location='media')