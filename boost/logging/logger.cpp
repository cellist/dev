#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/sinks/text_file_backend.hpp>
#include <boost/log/utility/setup/file.hpp>
#include <boost/log/utility/setup/common_attributes.hpp>
#include <boost/log/sources/severity_logger.hpp>
#include <boost/log/sources/record_ostream.hpp>
#include "Logger.h"

/* statische Elemente einer Klasse müssen initialisiert werden. */
Logger* Logger::_instance = NULL;

namespace blog = boost::log;

void Logger::Log(const level_t& level, std::string msg) {
  
  Logger::instance()->iLog(level, msg);
}

void Logger::iLog(const level_t& level, const std::string& msg) {
  blog::sources::severity_logger< blog::trivial::severity_level > lg;

  switch(level) {
  case Debug:
    BOOST_LOG_SEV(lg, blog::trivial::debug) << msg;
    break;
  case Info:
    BOOST_LOG_SEV(lg, blog::trivial::info) << msg;
    break;
  case Warn:
    BOOST_LOG_SEV(lg, blog::trivial::warning) << msg;
    break;
  case Error:
    BOOST_LOG_SEV(lg, blog::trivial::error) << msg;
    break;
  case Fatal:
    BOOST_LOG_SEV(lg, blog::trivial::fatal) << msg;
    break;
  default:
    BOOST_LOG_SEV(lg, blog::trivial::trace) << msg;
    break;
  }
}

Logger* Logger::instance() {
  if(!_instance) {
    _instance = new Logger();
    _instance->init();
    blog::add_common_attributes();
  }
  return _instance;
}

void Logger::init() {
  blog::add_file_log
    (
     blog::keywords::file_name = "app_%N.log",                                        /*< file name pattern >*/
     blog::keywords::rotation_size = 10 * 1024 * 1024,                                   /*< rotate files every 10 MiB... >*/
     blog::keywords::time_based_rotation = blog::sinks::file::rotation_at_time_point(0, 0, 0), /*< ...or at midnight >*/
     blog::keywords::format = "[%TimeStamp%]: %Message%"                                 /*< log record format >*/
     );
  
  blog::core::get()->set_filter
    (
     blog::trivial::severity >= blog::trivial::info
     );
}

int main(int argc, char* argv[]) {
  Logger::Log(Trace, "Hello, world ! <trace>");
  Logger::Log(Debug, "Hello, world ! <debug>");
  Logger::Log(Info,  "Hello, world ! <info>");
  Logger::Log(Warn,  "Hello, world ! <warn>");
  Logger::Log(Error, "Hello, world ! <error>");
  Logger::Log(Fatal, "Hello, world ! <fatal>");
  
  return 0;
}
