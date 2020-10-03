#ifndef WORD_FREQUENCY_H
#define WORD_FREQUENCY_H

// basic file operations
#include <iostream>
#include <fstream>

#include <algorithm>
#include <map>

/**
 * A word frequency calculator class
 */
class WordFrequency {
  
private:
  /// @param frequencies auxiliary map to compute the frequencies of individual words in input
  std::map<std::string, int> frequencies;
  
  /// @param wordCount keeping track of all words found in input
  int                        wordCount = 0;
  
public:
  /// standard class constructor
  WordFrequency();

  /**
   * Analyse a text file
   * @param inputFilename the path to the input text file
   */
  void ingest(const char* inputFilename);

  /**
   * Report on the result of the text file analysis
   */
  void report();
  
  /// standard class destructor
  ~WordFrequency();
};

#endif // WORD_FREQUENCY_H
