#include <log4cplus/logger.h>
#include <log4cplus/loglevel.h>
#include <log4cplus/loggingmacros.h>
#include <log4cplus/configurator.h>
#include <iomanip>

void printMessages(log4cplus::Logger const & logger)
{
  // Print messages using all common log levels.
  LOG4CPLUS_TRACE (logger, "printMessages()");
  LOG4CPLUS_DEBUG (logger, "This is a DEBUG message");
  LOG4CPLUS_INFO (logger, "This is a INFO message");
  LOG4CPLUS_WARN (logger, "This is a WARN message");
  LOG4CPLUS_ERROR (logger, "This is a ERROR message");
  LOG4CPLUS_FATAL (logger, "This is a FATAL message");
}

void thresholdTest(log4cplus::LogLevel ll)
{
  log4cplus::Logger logger
        = log4cplus::Logger::getInstance(LOG4CPLUS_TEXT("main"));

  // Set log level threshold on logger.
  logger.setLogLevel(ll);
  
  // Print messages.
    log4cplus::tcout
      << LOG4CPLUS_TEXT("*** calling printMessages() with ")
      << log4cplus::getLogLevelManager().toString(ll)
      << LOG4CPLUS_TEXT(" set: ***")
      << std::endl;
    printMessages(logger);
    log4cplus::tcout << std::endl;
}

int main()
{
  log4cplus::BasicConfigurator config;
  config.configure();
    
  thresholdTest(log4cplus::TRACE_LOG_LEVEL);
  thresholdTest(log4cplus::DEBUG_LOG_LEVEL);
  thresholdTest(log4cplus::INFO_LOG_LEVEL);
  thresholdTest(log4cplus::WARN_LOG_LEVEL);
  thresholdTest(log4cplus::ERROR_LOG_LEVEL);
  thresholdTest(log4cplus::FATAL_LOG_LEVEL);
  
  return 0;
}
