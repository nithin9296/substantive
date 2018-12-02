import datetime
AWS_ACCESS_KEY_ID = "AKIAJV3ELOAKWBU6H45Q"
AWS_SECRET_ACCESS_KEY = "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"
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'substantive.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'substantive.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'substantive-bucket'
S3DIRECT_REGION = 'ap-south-1'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_	_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = { 
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

AWS.config.update({
    signatureVersion: 'v4'
});