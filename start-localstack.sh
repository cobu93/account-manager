#!/bin/bash

# Install awslocal
pip install awscli-local[ver1] 

# Setup AWS S3
awslocal s3api create-bucket --bucket account-manager-test

cat > /tmp/cors-config.json << EOL
{
  "CORSRules": [
    {
      "AllowedHeaders": ["*"],
      "AllowedMethods": ["GET", "POST", "PUT"],
      "AllowedOrigins": ["*"],
      "ExposeHeaders": ["ETag"]
    }
  ]
}
EOL

cat /tmp/cors-config.json

awslocal s3api put-bucket-cors --bucket account-manager-test --cors-configuration file:///tmp/cors-config.json

# Create a user
awslocal iam create-user --user-name accmgr

# Create an access key
awslocal iam create-access-key --user-name accmgr


