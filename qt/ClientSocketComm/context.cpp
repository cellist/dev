#include <iostream>
#include <iterator>
#include <fstream>
#include <algorithm> // for std::copy

#include <QCommandLineParser>
#include <QtDebug>
#include <stdio.h>
#include "context.h"

Context::Context(QCoreApplication& app, int argc, char* argv[]) {

  /* Set default values */
  myHost          = "127.0.0.1";
  myPort          = 8080;
  myWaitMS        = 5000;
  myInputFilename = "datagrams.txt";
  mySleepTime     = 0;
  myMaxMsgs       = 0;
  myRnd           = NULL;
  myCommentChar   = '\0';
  
  this->processArgs(app, argc, argv);
}

Context::~Context() {

  qWarning() << "Context instance is garbage now.";
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

bool Context::keepSocketOpen() {
	return myKeepSocketOpen;
}

bool Context::handleComments(const std::string& in) {

  // Smartly detect comments and ignore them in input
  if(myCommentChar != '\0' &&
     in.at(0) == myCommentChar) {
    // We have a comment line here, ignore
    return false;
  }

  if(myMsgIndex == 0) {
    std::string valid_chars("%;+*-:#!?$/\\");
    int len = in.size();
    
    if(in.at(0) == in.at(len-1) &&
       std::string::npos != valid_chars.find(in.at(0))) {
      // We have a valid char that begins and ends the first line
      myCommentChar = in.at(0);
      qDebug() << "Input comment char is '" << in.at(0) << "'.";
      return false;
    }
  }

  // Not the first line any more - no comment indication
  return true;
}

bool Context::digestMessages() {

  myMsgIndex = 0;
  char buf[30];
  
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
      if (str.size() > 0  && handleComments(str)) {
	myMsgs.push_back(str);
	sprintf(buf,
		"datagram[%05d:%03lu]:",
		myMsgIndex,
		(unsigned long)str.size());
	qDebug() << buf << str.c_str();
	myMsgIndex++;
      }
    }

  in.close();
  myMsgIndex = 0;

  if (myConfirmTransmission) {
	  std::cout << "Press <RETURN> to start datagram transmission." << std::endl;
	  std::cin.get();
  }
  return true;
}

bool Context::noMoreMessages() {

	return myMaxMsgs < 1;
}

bool Context::getNextMessage(std::string& msg) {

  if (this->noMoreMessages()) {
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

  QCommandLineOption copt(QStringList() << "C" << "confirm",
	  QCoreApplication::translate("main", "press any key to confirm transmission after input has been read, default: send immediately"));
  parser.addOption(copt);

  QCommandLineOption hopt(QStringList() << "H" << "host",
			  QCoreApplication::translate("main", "host to connect to, default: 127.0.0.1"),
            QCoreApplication::translate("main", "host"));
  parser.addOption(hopt);

  QCommandLineOption iopt(QStringList() << "I" << "input-file",
			  QCoreApplication::translate("main", "take messages from <file>, default: datagrams.txt"),
            QCoreApplication::translate("main", "input-file"));
  parser.addOption(iopt);
    
  QCommandLineOption kopt(QStringList() << "K" << "keep-socket-open",
			  QCoreApplication::translate("main", "keep the socket open between transmissions, default: re-open for every datagram sent across"));
  parser.addOption(kopt);

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

  myConfirmTransmission = parser.isSet(copt);

  if(parser.isSet(hopt)) {
    myHost = parser.value(hopt);
  }
  
  if(parser.isSet(iopt)) {
    myInputFilename = parser.value(iopt);
  }

  myKeepSocketOpen = parser.isSet(kopt);
  
  if(parser.isSet(mopt)) {
    myMaxMsgs = parser.value(mopt).toInt();
    qWarning() << "Sending no more than" << myMaxMsgs << "messages to host.";
  }
  
  if(parser.isSet(popt)) {
    myPort = parser.value(popt).toInt();
  }

  if(parser.isSet(ropt)) {
    qWarning() << "Random mode is on.";
    myRnd = QRandomGenerator::system();
  }
  
  if(parser.isSet(sopt)) {
    mySleepTime = parser.value(sopt).toInt();
    qWarning() << "Going to sleep for" << mySleepTime
	       << "ms between message sends.";
  }
  
  if(parser.isSet(wopt)) {
    myWaitMS = parser.value(wopt).toInt();
  }
}
