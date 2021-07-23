#include <stdio.h>
#include <string.h>

void handle_options(int argc, char* argv[], char* dbname, size_t n) {
  
  int p = 0;
  while (++p < argc) {
    
    if (!strcmp(argv[p], "--db")) {
      p++;
      if (p >= argc) break;
      strncpy(dbname, argv[p], n);
    }
  }
}

int main(int argc, char* argv[]) {

  char dbname[20];

  handle_options(argc, argv, dbname, sizeof(dbname));

  printf("DB name is: >%s<\n", dbname);

  return 0;
}
