#ifndef _PAYLOAD_H_
#define _PAYLOAD_H_

#include <boost/shared_ptr.hpp>

class Payload;
typedef boost::shared_ptr<Payload> PayloadPtr;

class Payload {

 public:
  Payload();
  ~Payload();

  void inject(const PayloadPtr& ref);
  
 private:
  PayloadPtr reference;
};

#endif //  _PAYLOAD_H_
