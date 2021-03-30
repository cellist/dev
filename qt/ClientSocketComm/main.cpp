#include <QCommandLineParser>
#include <QtDebug>
#include <stdlib.h>
#include <iostream>

#include "context.h"
#include "client.h"

int main(int argc, char *argv[])
{
  QCoreApplication app(argc, argv);
  QCoreApplication::setApplicationName("Datagrams-over-TCP-socket sender");
  QCoreApplication::setApplicationVersion("1.0");
    
  Context ctx;
  Client client;
  QCommandLineParser parser;

  parser.setApplicationDescription("Datagrams-over-TCP-socket sender");
  parser.addHelpOption();
  parser.addVersionOption();

  QCommandLineOption hopt(QStringList() << "H" << "host",
			  QCoreApplication::translate("main", "host to connect to, default: localhost"),
            QCoreApplication::translate("main", "host"));
  parser.addOption(hopt);

  QCommandLineOption iopt(QStringList() << "I" << "input-file",
			  QCoreApplication::translate("main", "take messages from <file>, default: msg.txt"),
            QCoreApplication::translate("main", "input-file"));
  parser.addOption(iopt);

  QCommandLineOption mopt(QStringList() << "M" << "max-messages",
			  QCoreApplication::translate("main", "send at most <max> messages in total, default: 10000 (0: no limit)"),
            QCoreApplication::translate("main", "max"));
  parser.addOption(mopt);

  QCommandLineOption popt(QStringList() << "P" << "port",
			  QCoreApplication::translate("main", "port to connect to, default: 8080"),
            QCoreApplication::translate("main", "port"));
  parser.addOption(popt);
    
  QCommandLineOption ropt(QStringList() << "R" << "randomize",
			  QCoreApplication::translate("main", "send messages randomly, default: line by line from top to bottom"));
  parser.addOption(ropt);

  QCommandLineOption sopt(QStringList() << "S" << "sleep-between-sends",
			  QCoreApplication::translate("main", "sleep for <msec> ms between message sends, default: 0 (no waiting at all)"),
            QCoreApplication::translate("main", "msec"));
  parser.addOption(sopt);

  QCommandLineOption wopt(QStringList() << "W" << "wait",
			  QCoreApplication::translate("main", "wait for response with a maximum of <msec> ms before timing out, default: 5000"),
            QCoreApplication::translate("main", "msec"));
  parser.addOption(wopt);
  parser.process(app);
  
  if(parser.isSet(hopt)) ctx.setHost(parser.value(hopt));
  if(parser.isSet(iopt)) ctx.setInput(parser.value(iopt));
  if(parser.isSet(mopt)) ctx.setMsgMax(parser.value(mopt));
  if(parser.isSet(popt)) ctx.setPort(parser.value(popt));
  if(parser.isSet(ropt)) ctx.randomize();
  if(parser.isSet(sopt)) ctx.setSleep(parser.value(sopt));
  if(parser.isSet(wopt)) ctx.setWaitMS(parser.value(wopt));

  client.connectAndSend(ctx);

  std::cin.get();
  return 0;
}
