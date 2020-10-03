#include "word_frequency.h"

int main (int argc, char* argv[]) {
  const char* inputFilename = (argc == 1) ? "test_input.txt" : argv[argc-1];

  WordFrequency frequency;
  frequency.ingest(inputFilename);
  frequency.report();

  return 0;
}
