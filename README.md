# python-tesseract-ocr-lambda


#codebuild
image: aws/codebuild/eb-python-2.7-amazonlinux-64:2.1.6

#lambda
lambda configuration-->advanced-->timeout 30 seconds
runtime: python2.7
handler: app.lambda_handler

#s3 bucket setup
Properties-->Events: Name = lambdafunc
Properties-->Events: Events = ObjectCreate(All)
Properties-->Events: Send to = Lambda function
Properties-->Events: Lambda = Select your lambda function

````python
try:
    print("ver: " + tesserocr.tesseract_version())
    print("langs: " + tesserocr.get_languages())
    print("test: " + tesserocr.file_to_text('test.png'))
````    

# Test in docker - tbd
docker run -ti centos bash
yum install gcc gcc-c++ make wget -y
yum install autoconf aclocal automake -y
yum install libtool zip -y
yum install libjpeg-devel libpng-devel libtiff-devel zlib-devel -y
yum install git -y
yum install epel-release -y
yum install python-pip -y
yum install unzip -y
yum install centos-release-scl -y
yum install python27 -y
git clone https://github.com/tkntobfrk/python-tesseract-ocr-lambda.git
cd python*
chmod 755 build.sh
./build.sh
zip -g lambda.zip local.py
unzip lambda.zip -d $PWD/lambda
cd lambda
