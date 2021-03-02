#include <iostream>
#include "example.h"

void Counter::setValue(int value)
{
    if (value != m_value) {
        m_value = value;
        emit valueChanged(value);
    }
}

void info(Counter &a, Counter &b) {
  std::cout << "a.value(): " << a.value()
	    << ", b.value(): " << b.value() << std::endl;
}

int main() {
  Counter a, b;
  QObject::connect(&a, &Counter::valueChanged,
		   &b, &Counter::setValue);

  info(a, b);
  a.setValue(12);     // a.value() == 12, b.value() == 12
  info(a, b);
  b.setValue(48);     // a.value() == 12, b.value() == 48
  info(a, b);

  return 0;
}
