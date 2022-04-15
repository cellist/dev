/*
	calculator.c

	Example calculator service client in C

	Compilation in C (see samples/calc/calc.h):
	$ wsdl2h -c -o calc.h http://www.genivia.com/calc.wsdl
	$ soapcpp2 -CL calc.h
	$ cc -o calc calculator.c stdsoap2.c soapC.c soapClient.c
	$ ./calc add 2 3
	  result = 5
	where stdsoap2.c is in the 'gsoap' directory, or use libgsoap:
	$ cc -o calculator calculator.c soapC.c soapClient.c -lgsoap

--------------------------------------------------------------------------------
gSOAP XML Web services tools
Copyright (C) 2001-2017, Robert van Engelen, Genivia, Inc. All Rights Reserved.
This software is released under one of the following two licenses:
Genivia's license for commercial use.
--------------------------------------------------------------------------------
Product and source code licensed by Genivia, Inc., contact@genivia.com
--------------------------------------------------------------------------------
*/

#include "soapH.h"
#include "calc.nsmap"

const char server[] = "http://websrv.cs.fsu.edu/~engelen/calcserver.cgi";

int main(int argc, char **argv)
{
  struct soap soap;
  double a, b, result;

  if (argc < 4)
  { fprintf(stderr, "Usage: [add|sub|mul|div|pow] num num\n");
    exit(0);
  }

  soap_init1(&soap, SOAP_XML_INDENT);

  a = strtod(argv[2], NULL);
  b = strtod(argv[3], NULL);

  switch (*argv[1])
  { case 'a':
      soap_call_ns2__add(&soap, server, "", a, b, &result);
      break;
    case 's':
      soap_call_ns2__sub(&soap, server, "", a, b, &result);
      break;
    case 'm':
      soap_call_ns2__mul(&soap, server, "", a, b, &result);
      break;
    case 'd':
      soap_call_ns2__div(&soap, server, "", a, b, &result);
      break;
    case 'p':
      soap_call_ns2__pow(&soap, server, "", a, b, &result);
      break;
    default:
      fprintf(stderr, "Unknown command\n");
      exit(0);
  }
  if (soap.error)
    soap_print_fault(&soap, stderr);
  else
    printf("result = %g\n", result);

  soap_destroy(&soap);
  soap_end(&soap);
  soap_done(&soap);

  return 0;
}
