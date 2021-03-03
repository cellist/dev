#include "mythread.h"
#include <QDebug>

MyThread::MyThread(QString s) : name(s)
{
}

// We overrides the QThread's run() method here
// run() will be called when a thread starts
// the code will be shared by all threads

void MyThread::run()
{
    for(int i = 0; i <= 100; i++)
    {
        qDebug() << this->name << " " << i;
    }
}
