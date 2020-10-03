#ifndef WORD_FREQUENCY_H
#define WORD_FREQUENCY_H

// basic file operations
#include <iostream>
#include <fstream>

#include <algorithm>
#include <map>

class WordFrequency {
  
private:
  // auxiliary map to compute the frequencies of individual words in input
  std::map<std::string, int> myFrequencies;
  int                        myWordCount = 0;
  
public:
  void ingest(const char* inputFilename);
  void report();
};

#endif // WORD_FREQUENCY_H
