#ifndef _LOGGER_H_
#define _LOGGER_H_

#include <string>

typedef enum { Trace=0, Debug, Info, Warn, Error, Fatal } level_t;

class Logger {
 public:
  static void Log(const level_t& level, std::string msg);

 private:
  void init();
  void iLog(const level_t& level, const std::string& msg);
  
  static Logger* instance();
  static Logger* _instance;

  /* Logger must not be created externally */
  Logger () { }
  // Move to "protected", if inheritance shall be supported
  Logger ( const Logger& ); /* A second instance must not be
			       created via copy-construction */
};

#endif /* _LOGGER_H_ */
