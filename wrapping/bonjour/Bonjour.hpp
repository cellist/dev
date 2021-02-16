// https://flanusse.net/interfacing-c++-with-python.html

#include <iostream>
#include <string>

class Bonjour
{
private:
  // Private attribute
  std::string m_msg;
  
public:
  // Constructor
  Bonjour(std::string msg):m_msg(msg) { }
  
  // Methods
  void greet();
  
  // Getter/Setter functions for the attribute
  void set_msg(std::string msg);
  std::string get_msg() const;
};
