# Image Resizer for AWS Lambda

This is a python image resizer to be run on an AWS Lamda S3 event trigger

## To add additional packages:

'''bash
pip install \
--platform manylinux2014_x86_64 \
--target=package \
--implementation cp \
--python-version 3.9.12 \
--only-binary=:all: --upgrade \
<package_name>
'''

## To zip packages & .py file into folder for S3 deployment

'''bash
cd package
'''

'''bash
zip -r ../my_deployment_package.zip .
'''

'''bash
cd ..
'''

'''bash
zip my_deployment_package.zip Resizeimage.py
'''

## Reference Docs
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html 