#include <iostream>
#include "payload.h"

Payload::Payload() {

  std::cout << "Payload(): "
	    << this->reference.use_count() << std::endl;
}

Payload::~Payload() {

  std::cout << "~Payload(): "
	    << this->reference.use_count() << std::endl;
}

void Payload::inject(const PayloadPtr& ref) {

  std::cout << "Payload::inject: "
	    << this->reference.use_count() << std::endl;
}
