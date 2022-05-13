#!/bin/sh
rm -f *~ hello.cgi ns.hello.req.xml ns.hello.res.xml \
ns.nsmap ns.wsdl ns.xsd soapC.cppsoapClient.cpp \
soapClientLib.cpp soapH.h soapServer.cpp soapServerLib.cpp \
soapStub.h soapC.cpp  soapClient.cpp myapp

soapcpp2 hello.h
clang++ -o hello.cgi hello.cpp soapC.cpp soapServer.cpp -lgsoap++
clang++  -o myapp myapp.cpp soapC.cpp soapClient.cpp -lgsoap++
