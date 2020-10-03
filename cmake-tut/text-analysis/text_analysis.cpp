#include "word_frequency.h"

/**
 * This is a small proof-of-concept sample.
 * Its purpose is to try out the cmake tool,
 * and to recap OOP in C++.
 * The scenario used is a word frequency detector.
 * This path to the input file is the only parameter to this program.
 */
int main (int argc, char* argv[]) {
  const char* inputFilename = (argc == 1) ? "test_input.txt" : argv[argc-1];

  WordFrequency frequency;
  frequency.ingest(inputFilename);
  frequency.report();

  return 0;
}
