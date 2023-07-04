/*
* threads.cxx
*/
#include "work.h"
 
int main()
{
  Work* work = new Work();
  work->go(); 
  delete work; 
  return 0;
}
