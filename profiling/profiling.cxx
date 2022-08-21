// $ g++ -pg -pedantic -Wall -o profiling profiling.cxx deepthought.cxx
// $ ./profiling
// $ gprof profiling gmon.out | less
//
#include <iostream>
#include "deepthought.h"

int main() {
  unsigned int seed = 42;
  DeepThought* dt = new DeepThought();
  
  for(unsigned int i = 0; i < 100; i++) {
    std::cout << i << ": " << seed << std::endl;
    
    seed = dt->thinkAbout(seed);
  }

  delete dt;
  return 0;
}
