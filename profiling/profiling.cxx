// $ g++ -pg -pedantic -Wall -o profiling profiling.cxx
// $ ./profiling
// $ gprof profiling gmon.out | less
//
#include <iostream>

unsigned int compute1(const unsigned int x);
unsigned int compute2(const unsigned int x);
unsigned int compute3(const unsigned int x);
unsigned int compute5(const unsigned int x);
unsigned int compute7(const unsigned int x);
unsigned int compute11(const unsigned int x);

unsigned int compute1(const unsigned int x) {
  
  return 400-x;
}

unsigned int compute2(const unsigned int x) {

  return (x%3) ? 2*x-1 : compute3(x+1);
}

unsigned int compute3(const unsigned int x) {
  
  return (x%5) ? 2*x-2 : compute5(x+1);
}

unsigned int compute5(const unsigned int x) {

  return (x%7) ? 2*x-3 : compute7(x+1);
}

unsigned int compute7(const unsigned int x) {

  return (x%11) ? 2*x-4 : compute11(x+1);
}

unsigned int compute11(const unsigned int x) {

  return 2*x-5;
}

unsigned int newSeed(const unsigned int x) {
  
  unsigned int answer = 0;

  if(x > 200) {
    answer = compute1(x);
  } else if(!(x%2)) {
    answer = compute2(x);
  } else if(!(x%3)) {
    answer = compute3(x);
  } else if(!(x%5)) {
    answer = compute5(x);
  } else {
    answer = compute7(x);
  }
  
  return answer;
}

int main() {
  unsigned int seed = 42;
  
  for(unsigned int i = 0; i < 100; i++) {
    std::cout << i << ": " << seed << std::endl;
    
    seed = newSeed(seed);
  }
  
  return 0;
}
