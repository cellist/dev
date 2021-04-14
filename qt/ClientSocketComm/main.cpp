#include <QTime>
#include <QtDebug>
#include <stdlib.h>
#include <iostream>

#include "context.h"
#include "client.h"

void myMessageOutput(QtMsgType type,
		     const QMessageLogContext& context,
		     const QString& msg)
{
  QString     timeStamp = QTime::currentTime().toString("hh:mm:ss.zzz");
  std::string theMsg = msg.toStdString();
  char        level[] = "DWCFI";
  
  switch (type) {
  case QtDebugMsg:
  case QtInfoMsg:
  case QtWarningMsg:
  case QtCriticalMsg:
  case QtFatalMsg:
    std::cerr << "[" << timeStamp.toStdString() << " "
	      << level[type%(sizeof(type)/sizeof(char))] << "] "
	      << theMsg << std::endl;
    break;
  }
}

int main(int argc, char *argv[])
{
  qInstallMessageHandler(myMessageOutput);
  QCoreApplication app(argc, argv);
  QCoreApplication::setApplicationName("Datagrams-over-TCP-socket sender");
  QCoreApplication::setApplicationVersion("1.0");
    
  Context ctx(app, argc, argv);
  Client client;

  client.connectAndSend(ctx);

  std::cout << "Press <RETURN> to exit." << std::endl;
  std::cin.get();
  return 0;
}
