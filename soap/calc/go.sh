#!/bin/sh
rm -f \
   *~ calc *xml calc.nsmap soapC.c soapClient.c soapClientLib.c \
   soapH.h soapServer.c soapServerLib.c soapStub.h

wsdl2h -c -o calc.h http://www.genivia.com/calc.wsdl
soapcpp2 -CL calc.h
clang -o calc calc.c soapClient.c soapC.c -lgsoap
./calc add 42 33
