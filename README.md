# python-tesseract-ocr-lambda

Need to update PSM for different types use centos-release-scl

https://github.com/tesseract-ocr/tesseract/wiki/ImproveQuality#page-segmentation-method

# codebuild
````text
image: aws/codebuild/eb-python-2.7-amazonlinux-64:2.1.6
````

# lambda
````text
lambda configuration-->advanced-->timeout 30 seconds
runtime: python2.7
handler: app.lambda_handler
````

# s3 bucket setup
````text
Properties-->Events: Name = lambdafunc
Properties-->Events: Events = ObjectCreate(All)
Properties-->Events: Send to = Lambda function
Properties-->Events: Lambda = Select your lambda function
````

# EC2 instance build
````bash
sudo su
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
````

# Test in docker - tbd
````bash
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
````

# Should be able to run this through docker this way too
docker run -v "$PWD":/var/task lambci/lambda:python2.7 app.myHandler '{"some": "event"}'

# python examples tbd
````python
try:
    print("ver: " + tesserocr.tesseract_version())
    print("langs: " + tesserocr.get_languages())
    print("test: " + tesserocr.file_to_text('test.png'))
````    
