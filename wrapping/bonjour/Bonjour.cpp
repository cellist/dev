#include "Bonjour.hpp"

void Bonjour::greet() {
  std::cout << m_msg << std::endl;
}

void Bonjour::set_msg(std::string msg) {
  this->m_msg = msg;
}

std::string Bonjour::get_msg() const {
  return m_msg;
}
