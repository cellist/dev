#include <iostream>
#include <errno.h>
#include "greeter.h"

int main()
{
    Greeter greetMe;

    std::cout << "program invocation name: "
	      << program_invocation_name << std::endl
	      << "program invocation short name: "
	      << program_invocation_short_name << std::endl;
    
    greetMe.greet();
    return 0;
}
