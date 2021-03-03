// https://www.bogotobogo.com/Qt/Qt5_QThreads_Creating_Threads.php
#include <QCoreApplication>
#include "mythread.h"

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    
    MyThread thread1("A"), thread2("B"), thread3("C");

    thread1.start();
    thread2.start();
    thread3.start();

    return a.exec();
}
