/*
* work.h
*/
#ifndef _WORK_H_
#define _WORK_H_
 
#include <string>
#include <thread>
 
class Work {
public:
    Work();
    ~Work();
    void go();
 
private:
    static void task1(std::string msg, int howOften);
    static void task2(std::string msg, int howOften);
    static void do_work1();
    static void do_work2();
    
    std::thread* m_t1;
    std::thread* m_t2;
};
#endif
