// hello.cpp
#include "soapH.h"  // include the generated source code headers
#include "ns.nsmap" // include XML namespaces
int main()
{
  return soap_serve(soap_new());
}
int ns__hello(struct soap *soap, std::string name, std::string& greeting)
{
  greeting = "Hello " + name;
  return SOAP_OK;
}
