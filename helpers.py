import boto3, botocore
import braintree
from config import S3_KEY, S3_SECRET, S3_BUCKET, BT_MERCHANT, BT_PUBLIC, BT_PRIVATE

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

gateway = braintree.BraintreeGateway(
	braintree.Configuration(
		braintree.Environment.Sandbox,
		merchant_id=BT_MERCHANT,
		public_key=BT_PUBLIC,
		private_key=BT_PRIVATE
	)
)
