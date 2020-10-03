#include "word_frequency.h"

WordFrequency::WordFrequency() {
  std::cout << "Word frequency object " << this
	    << " is instantiated." << std::endl;
}

WordFrequency::~WordFrequency() {
  std::cout << "Word frequency instance " << this
	    << " is being discarded." << std::endl;
}

void WordFrequency::ingest(const char* inputFilename) {
  std::ifstream someFile;
  std::string   someWord, cleansedWord;
  
  someFile.open (inputFilename, std::ios::in);
  
  if (someFile.is_open()) {
    std::cout << "File " << inputFilename
	      << " has been opened successfully." << std::endl;
    
    while(someFile >> someWord) {
      this->wordCount++;
      // convert current word to lower case
      std::transform(someWord.begin(),
		     someWord.end(),
		     someWord.begin(),
		     [](unsigned char const &c){
		       return ::tolower(c);
		     });
      
      // remove anything that is not alphanumeric
      std::copy_if(someWord.begin(),
		   someWord.end(),
		   std::back_inserter(cleansedWord),
		   [](char ch) { return isalnum(ch); });
	
      // adjust frequency with cleansed word
      if(this->frequencies.find(cleansedWord) == this->frequencies.end()) {
	this->frequencies.insert(make_pair(cleansedWord, 1));
      } else {
	this->frequencies[cleansedWord]++;
      }
      
      cleansedWord.erase(cleansedWord.begin(),cleansedWord.end());
    } // while some word
    
    someFile.close();
  } // if file open
}

void WordFrequency::report() {  
  // do the reporting
  std::cout << "Input file had " << this->wordCount
	    << " words in it, " << this->frequencies.size()
	    << " of them were different." << std::endl;
  
  for(auto& freqPairs : this->frequencies) {
    std::cout << freqPairs.first << ": " << freqPairs.second << std::endl;
  }
}
