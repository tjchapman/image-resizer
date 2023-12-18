# image-resizer
Python script to resize jpg &amp; png files using AWS Lambda

## To add additional packages

```
pip install \
--platform manylinux2014_x86_64 \
--target=package \
--implementation cp \
--python-version 3.9.12 \
--only-binary=:all: --upgrade \
<package_name>

```

## To zip packages & .py file into folder for S3 deployment

```
cd package
```

```
zip -r ../my_deployment_package.zip .
```

```
cd ..
```

```
zip my_deployment_package.zip Resizeimage.py
```

## Reference Docs
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html 
