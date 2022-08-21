#ifndef _DEEPTHOUGHT_H_
#define _DEEPTHOUGHT_H_

class DeepThought {

public:
  DeepThought();
  ~DeepThought();
  
  unsigned int thinkAbout(const unsigned int x);

private:
  unsigned int compute1(const unsigned int x);
  unsigned int compute2(const unsigned int x);
  unsigned int compute3(const unsigned int x);
  unsigned int compute5(const unsigned int x);
  unsigned int compute7(const unsigned int x);
  unsigned int compute11(const unsigned int x);
};

#endif // _DEEPTHOUGHT_H_
