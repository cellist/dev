#include <boost/python.hpp>

/*
https://stackoverflow.com/questions/43387112/wrapping-c-code-with-python-manually#43387190
https://flanusse.net/interfacing-c++-with-python.html
*/

char const *firstMethod() {
  return "This is the first try.";
}

BOOST_PYTHON_MODULE(libcallme) {
  // boost::python is the namespace
  boost::python::def("getTryString", firstMethod);
}
