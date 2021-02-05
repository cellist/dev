/*
** Credits go to Chris Gregg!
** https://www.youtube.com/watch?v=A5Rc4AwdaOA
**
** gcc -g -Og memoryLeak.c -o memoryLeak
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

const int ARR_SIZE = 1000;

int main() {

  /*
    Create an array to hold ARR_SIZE integers
    and populate it.
  */
  int irandom, *iA = malloc(sizeof(int) * ARR_SIZE);
  for( int i = 0; i < ARR_SIZE; i++ ) {
    iA[i] = i;
  }

  /* Pick a random element and print it */
  srand(time(NULL));
  irandom = rand() % ARR_SIZE;
  printf("Array[%d]: %d\n", irandom, iA[irandom]);

  /*
    dang!!!
    free(iA);
  */
  return 0;
}
