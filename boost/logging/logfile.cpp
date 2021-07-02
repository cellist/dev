// https://www.boost.org/doc/libs/1_75_0/libs/log/doc/html/log/tutorial/sinks.html

/*
 *          Copyright Andrey Semashev 2007 - 2015.
 * Distributed under the Boost Software License, Version 1.0.
 *    (See accompanying file LICENSE_1_0.txt or copy at
 *          http://www.boost.org/LICENSE_1_0.txt)
 */

#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/sinks/text_file_backend.hpp>
#include <boost/log/utility/setup/file.hpp>
#include <boost/log/utility/setup/common_attributes.hpp>
#include <boost/log/sources/severity_logger.hpp>
#include <boost/log/sources/record_ostream.hpp>

namespace blog = boost::log;

void init()
{
  blog::add_file_log
    (
     blog::keywords::file_name = "sample_%N.log",                                        /*< file name pattern >*/
     blog::keywords::rotation_size = 10 * 1024 * 1024,                                   /*< rotate files every 10 MiB... >*/
     blog::keywords::time_based_rotation = blog::sinks::file::rotation_at_time_point(0, 0, 0), /*< ...or at midnight >*/
     blog::keywords::format = "[%TimeStamp%]: %Message%"                                 /*< log record format >*/
     );

  blog::core::get()->set_filter
    (
     blog::trivial::severity >= blog::trivial::info
     );
}

int main(int, char*[])
{
  init();
  blog::add_common_attributes();
  blog::sources::severity_logger< blog::trivial::severity_level > lg;

  BOOST_LOG_SEV(lg, blog::trivial::trace) << "A trace severity message";
  BOOST_LOG_SEV(lg, blog::trivial::debug) << "A debug severity message";
  BOOST_LOG_SEV(lg, blog::trivial::info) << "An informational severity message";
  BOOST_LOG_SEV(lg, blog::trivial::warning) << "A warning severity message";
  BOOST_LOG_SEV(lg, blog::trivial::error) << "An error severity message";
  BOOST_LOG_SEV(lg, blog::trivial::fatal) << "A fatal severity message";

  return 0;
}
