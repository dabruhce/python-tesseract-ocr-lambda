#!/bin/sh -x
export BUILD_DIR=$PWD

#BUILD LEPTONICA
wget http://www.leptonica.com/source/leptonica-1.73.tar.gz
tar -zxvf leptonica-1.73.tar.gz
cd leptonica-1.73/
./autobuild
./configure
make
make install
ldconfig
cd ..

#BUILD TESSERACT
wget https://github.com/tesseract-ocr/tesseract/archive/3.04.01.tar.gz
tar -zxvf 3.04.01.tar.gz
cd tesseract-3.04.01
./autogen.sh
./configure
make
make install
cd ..

mkdir tesseracts
pip install virtualenv
virtualenv env
source env/bin/activate
pip install cython
CPPFLAGS=-I/usr/local/include pip install tesserocr
pip install -r requirements.txt
pip install logging

#package tess
cd tesseracts
cp /usr/local/bin/tesseract .
cp -r $BUILD_DIR/env/lib64/python2.7/site-packages/. .
mkdir lib
cd lib
cp /usr/local/lib/libtesseract.so.3 .
cp /usr/local/lib/liblept.so.5 .
cp /lib64/librt.so.1 .
cp /lib64/libz.so.1 .
cp /usr/lib64/libpng12.so.0 .
cp /usr/lib64/libjpeg.so.62 .
cp /usr/lib64/libtiff.so.5 .
cp /lib64/libpthread.so.0 .
cp /usr/lib64/libstdc++.so.6 .
cp /lib64/libm.so.6 .
cp /lib64/libgcc_s.so.1 .
cp /lib64/libc.so.6 .
cp /lib64/ld-linux-x86-64.so.2 .
cp /usr/lib64/libjbig.so.2.0 .
cd ..
mkdir tessdata
cd tessdata
cp $BUILD_DIR/tessdata/eng.traineddata .
cd ..
cd ..

cd tesseracts
zip -r $BUILD_DIR/lambda.zip .
cd ..
zip -g lambda.zip app.py
zip -g lambda.zip test.png

#zip -r all.zip .
