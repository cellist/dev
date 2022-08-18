// g++ -g --pedantic -Wall -o echotime echotime.cxx

#include <iostream>
#include <ctime>
#include <iomanip>
#include <unistd.h>

short echoTime() {
  time_t now = time(0);
  static short c = 0;
   
  // convert now to string form
  char* dt = ctime(&now);

  std::cout << std::setfill('0') << std::setw(2) << c
	    << ": the local date and time is: " << dt;

  // convert now to tm struct for UTC
  tm *gmtm = gmtime(&now);
  dt = asctime(gmtm);
  std::cout << std::setfill('0') << std::setw(2) << c
	    << ": the UTC date and time is:"<< dt << std::endl;
  
  return ++c;
}

int main() {
  const short MAXITER = 50;
  const short SNOOZE  = 5;
  
  while(MAXITER > echoTime()) {
    sleep(SNOOZE);
  }

  return 0;
}
