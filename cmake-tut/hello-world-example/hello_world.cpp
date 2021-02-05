#include <iostream>
#include <string>

class Greeter {
    public:
        Greeter();
        ~Greeter();
        void greet() const;

    private:
        std::string myGreeting;
};

Greeter::Greeter() {
    this->myGreeting = "Hello, world!";
}

Greeter::~Greeter() {
    std::cout << "Goodbye." << std::endl;
}

void Greeter::greet() const {
        std::cout << this->myGreeting << std::endl;
}

int main()
{
    Greeter greetMe;

    greetMe.greet();
    return 0;
}
