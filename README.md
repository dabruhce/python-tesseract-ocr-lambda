# tesseract-ocr-lambda


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
