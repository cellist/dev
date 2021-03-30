#include <iostream>
#include <iterator>
#include <fstream>
#include <algorithm> // for std::copy

#include <QCommandLineParser>
#include <QtDebug>
#include "context.h"

Context::Context(QCoreApplication& app, int argc, char* argv[]) {

  /* Set default values */
  myHost          = "localhost";
  myPort          = 8080;
  myWaitMS        = 5000;
  myInputFilename = "msg.txt";
  mySleepTime     = 0;
  myMaxMsgs       = 0;
  myRnd           = NULL;

  this->processArgs(app, argc, argv);
}

Context::~Context() {

  qDebug() << "Context instance is garbage now.";
}

uint Context::getPort() {
  return myPort;
}

QString Context::getHost() {
  return myHost;
}

uint Context::getWaitMS() {
  return myWaitMS;
}

ulong Context::getSleep() {
  return mySleepTime;
}

bool Context::digestMessages() {

  myMsgIndex = 0;

  // Open the File
  std::ifstream in(myInputFilename.toStdString());
  // Check if object is valid
  if (!in)
    {
      qDebug() << "Cannot open " << myInputFilename << " for input!";
      return false;
    }
  std::string str;
  // Read the next line from File until it reaches the end.
  while (std::getline(in, str))
    {
      // Line contains string of length > 0 then save it in vector
      if (str.size() > 0)
	myMsgs.push_back(str);
    }
  //Close The File
  in.close();
  return true;
}

bool Context::getNextMessage(std::string& msg) {

  if (myMaxMsgs < 1) {
    qDebug() << "Maximum number of messages sent, stopping now.";

    return false;
  }

  myMaxMsgs--;

  if (!myMsgs.size()) {
    this->digestMessages();
  }

  if (myRnd) {
    myMsgIndex = myRnd->generate() % myMsgs.size();
    msg = myMsgs.at(myMsgIndex);

    return true;
  } else if (myMsgIndex < myMsgs.size()) {
    msg = myMsgs.at(myMsgIndex);
    myMsgIndex++;

    return true;
  }
  return false;
}

uint Context::getMsgIndex() {

  return myMsgIndex;
}

void Context::processArgs(QCoreApplication& app, int argc, char* argv[]) {
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
  
  if(parser.isSet(hopt)) {
    myHost = parser.value(hopt);
  }
  
  if(parser.isSet(iopt)) {
    myInputFilename = parser.value(iopt);
  }

  if(parser.isSet(mopt)) {
    myMaxMsgs = parser.value(mopt).toInt();
    qDebug() << "Sending no more than" << myMaxMsgs << "messages to host.";
  }
  
  if(parser.isSet(popt)) {
    myPort = parser.value(popt).toInt();
  }

  if(parser.isSet(ropt)) {
    qDebug() << "Random mode is on.";
    myRnd = QRandomGenerator::system();
  }
  
  if(parser.isSet(sopt)) {
    mySleepTime = parser.value(sopt).toInt();
    qDebug() << "Going to sleep for" << mySleepTime
	     << "ms between message sends.";
  }
  
  if(parser.isSet(wopt)) {
    myWaitMS = parser.value(wopt).toInt();
  }
}
