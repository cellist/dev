/*
 * work.cpp
 */
#include <iostream>
#include <chrono>
#include <pqxx/pqxx>

#include "work.h"

void Work::do_work1()
{
  try
    {
      pqxx::connection c;
      pqxx::work w(c);
      pqxx::result result = w.exec(
				   "SELECT id, transfrom, transto,"
				   " fromterm, toterm"
				   " FROM translations"
				   );
      w.commit();
      for (auto row = std::begin(result); row != std::end(result); row++)
	{
	  std::cout << "| ";
	  for (auto field = std::begin(row); field != std::end(row); field++)
	    {
	      std::cout << field->c_str() << " | ";
	    }
	  std::cout << std::endl;
	}
    }
  catch (std::exception const &e)
    {
      std::cerr << e.what() << std::endl;
    }
}

void Work::do_work2()
{
  try
    {
      pqxx::connection c;
      pqxx::work w(c);
      pqxx::result result = w.exec(
				   "SELECT id, aconcept, atag"
				   " FROM tags"
				   " WHERE atag NOT LIKE '%e%'"
				   );
      w.commit();
      for (auto row = std::begin(result); row != std::end(result); row++)
	{
	  std::cout << "| ";
	  for (auto field = std::begin(row); field != std::end(row); field++)
	    {
	      std::cout << field->c_str() << " | ";
	    }
	  std::cout << std::endl;
	}
    }
  catch (std::exception const &e)
    {
      std::cerr << e.what() << std::endl;
    }
}

void Work::task1(std::string msg, int howOften)
{
  using namespace std::chrono_literals;
 
  while (howOften > 0) {
    const auto start = std::chrono::high_resolution_clock::now();
    do_work1();
    std::this_thread::sleep_for(4800ms);
    const auto end = std::chrono::high_resolution_clock::now();
    const std::chrono::duration<double, std::milli> elapsed = end - start;
 
    std::cout << --howOften << msg << elapsed.count() << "ms" << std::endl;
  }
}
 
void Work::task2(std::string msg, int howOften)
{
  using namespace std::chrono_literals;
 
  while (howOften > 0) {
    const auto start = std::chrono::high_resolution_clock::now();
    do_work2();
    std::this_thread::sleep_for(5200ms);
    const auto end = std::chrono::high_resolution_clock::now();
    const std::chrono::duration<double, std::milli> elapsed = end - start;
 
    std::cout << --howOften << msg << elapsed.count() << "ms" << std::endl;
  }
}
 
Work::Work() {
  m_t1 = NULL;
  m_t2 = NULL;
  std::cout << "Work has been created." << std::endl;
}
 
 
Work::~Work() {
  if (m_t1) {
    // Makes the main thread wait for the new thread to finish execution, therefore blocks its own execution.
    m_t1->join();
    delete m_t1;
    m_t1 = NULL;
  }
 
  if (m_t2) {
    m_t2->join();
    delete m_t2;
    m_t2 = NULL;
  }
 
  std::cout << "Work has shut down." << std::endl;
}
 
void Work::go()
{
  // Constructs the new thread and runs it. Does not block execution.
  m_t1 = new std::thread(Work::task1, ": <Work::task1> Waited for ", 100);
 
  // Constructs the new thread and runs it. Does not block execution.
  m_t2 = new std::thread(Work::task2, ": <Work::task2> Waited for ", 100);
}
