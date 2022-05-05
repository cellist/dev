#include <iostream>
#include "payload.h"

int main() {

  PayloadPtr p(new Payload());
  std::cout << "main 1: "
	    << p.use_count() << std::endl;

  p->inject(p);
  std::cout << "main 2: "
	    << p.use_count() << std::endl;
  
  return 0;
}
