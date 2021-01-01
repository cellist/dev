/*
** Decompose integer numbers into their prime factors
*/

#include <iostream>

void decompose(long int& num, long int start) {

  for(; start*start <= num; start++) {
    if(num%start == 0) {
      num/=start;
      std::cout << start << "(" << num << ") ";
      decompose(num, start);
      break;
    }
   }
}

int main(int argc, char* argv[]) {

  const char prompt[] = "Enter a non-negative number to calculate its factors: ";
  long int num;
  int iterations = 0;

  std::cout << prompt;
  while(std::cin >> num) {
    if(num < 1) break;
    iterations++;
    decompose(num, 2);
    std::cout << num << "(1)" << std::endl << prompt;
  }

  std::cout << iterations << " iterations." << std::endl;
}
