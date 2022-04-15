#include "soapH.h"
#include "ns.nsmap" // include XML namespaces

int main(int argc, char* argv[]) {
  struct soap *soap = soap_new(); // new context
  std::string greeting;
  if (soap_call_ns__hello(soap, "http://yourdomain/cgi/hello.cgi", NULL, "world", greeting) == SOAP_OK)
    std::cout << greeting << std::endl;
  else
    soap_stream_fault(soap, std::cerr);
  soap_destroy(soap); // delete managed deserialized C++ instances
  soap_end(soap);     // delete other managed data
  soap_free(soap);    // free context

  return 0;
}
