// main.cpp
// https://www.bogotobogo.com/Qt/Qt5_QTcpSocket.php

#include <QCoreApplication>
#include "mytcpsocket.h"

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    
    MyTcpSocket s;
    s.doConnect();
            
    return a.exec();
}
