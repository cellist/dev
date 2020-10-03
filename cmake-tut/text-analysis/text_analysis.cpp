// basic file operations
#include <iostream>
#include <fstream>

#include <algorithm>
#include <map>

int main (int argc, char* argv[]) {
  std::map<std::string,int> frequency;      
  std::ifstream             someFile;
  std::string               someWord, cleansedWord;
  int                       words = 0;
  const char*               inputFilename = (argc == 1) ?
    "test_input.txt" :
    argv[argc-1];

  someFile.open (inputFilename, std::ios::in);
  
  if (someFile.is_open()) {
    std::cout << "File " << inputFilename
	      << " has been opened successfully." << std::endl;
  
    while(someFile >> someWord) {
      words++;
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
      if(frequency.find(cleansedWord) == frequency.end()) {
	frequency.insert(make_pair(cleansedWord, 1));
      } else {
	frequency[cleansedWord]++;
      }
      
      cleansedWord.erase(cleansedWord.begin(),cleansedWord.end());
    }
  
    someFile.close();

    // do the reporting
    std::cout << "Input " << inputFilename << " had "
	      << words << " words in it, " << frequency.size()
	      << " of them were different." << std::endl;
    
    for(auto& freqPairs : frequency) {
      std::cout << freqPairs.first << ": " << freqPairs.second << std::endl;
    }
  }

  return 0;
}
