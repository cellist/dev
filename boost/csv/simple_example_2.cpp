// https://www.boost.org/doc/libs/1_74_0/libs/tokenizer/doc/escaped_list_separator.htm

// simple_example_2.cpp
#include<iostream>
#include<boost/tokenizer.hpp>
#include<string>

int main(){
  std::string csv = "Field 1,\"putting quotes around fields, allows commas\",Field 3";

  boost::tokenizer<boost::escaped_list_separator<char> > tok(csv);
  for(boost::tokenizer<boost::escaped_list_separator<char> >::iterator beg = tok.begin();
      beg != tok.end();
      ++beg){
    std::cout << *beg << std::endl;
  }
}
