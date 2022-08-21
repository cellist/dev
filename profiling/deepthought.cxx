#include <iostream>
#include "deepthought.h"

DeepThought::DeepThought() {
  std::cout << "Deep Thought at your service ..." << std::endl;
}

DeepThought::~DeepThought() {
  std::cout << "Have a nice day and don't panic!" << std::endl;
}

unsigned int DeepThought::compute1(const unsigned int x) {
  
  return 2+3+5+7+x%42;
}

unsigned int DeepThought::compute2(const unsigned int x) {

  return (x%3) ? 2*x-1 : compute3(x+1);
}

unsigned int DeepThought::compute3(const unsigned int x) {
  
  return (x%5) ? 2*x-2 : compute5(x+1);
}

unsigned int DeepThought::compute5(const unsigned int x) {

  return (x%7) ? 2*x-3 : compute7(x+1);
}

unsigned int DeepThought::compute7(const unsigned int x) {

  return (x%11) ? 2*x-4 : compute11(x+1);
}

unsigned int DeepThought::compute11(const unsigned int x) {

  return 2*x-5;
}

unsigned int DeepThought::thinkAbout(const unsigned int x) {
  
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
