#ifndef __GREETER_H__
#define __GREETER_H__

#include <string>

class Greeter {
    public:
        Greeter();
        ~Greeter();
        void greet() const;

    private:
        std::string myGreeting;
};

#endif // #ifndef __GREETER_H__