#include <iostream>
#include "greeter.h"

Greeter::Greeter() {
    this->myGreeting = "Hello, world!";
}

Greeter::~Greeter() {
    std::cout << "Goodbye." << std::endl;
}

void Greeter::greet() const {
    std::cout << this->myGreeting << std::endl;
}
