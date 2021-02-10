// Borrowing from:
// https://www.learncpp.com/cpp-tutorial/code-coverage/
#include <iostream>

int foo(int x, int y)
{
  int z{ y };
  if (x > y)
    {
      z = x;
    }
  return z;
}

bool isLowerVowel(char c)
{
  switch (c) // statement 1
    {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
      return true; // statement 2
    default:
      return false; // statement 3
    }
}

void compare(int x, int y)
{
  if (x > y)
    std::cout << x << " is greater than " << y << std::endl;
  else if (x < y)
    std::cout << x << " is less than " << y << std::endl;
  else
    std::cout << x << " is equal to " << y << std::endl;
}

int howDareYou()
{
  return -1;
}

int main(int argc, char* argv[]) {
  
  // execute some code, but not all
  std::cout << foo(1,2) << std::endl;
  std::cout << isLowerVowel('Q') << std::endl;
  compare(0,1);
  compare(1,0);

  return 0;
}
