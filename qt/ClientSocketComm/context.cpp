#include <iostream>
#include <iterator>
#include <fstream>
#include <algorithm> // for std::copy
#include <QtDebug>
#include "context.h"

Context::Context() {

  /* Set default values */
  myHost          = "localhost";
  myPort          = 8080;
  myWaitMS        = 5000;
  myInputFilename = "msg.txt";
  mySleepTime     = 0;
  myMaxMsgs       = 0;
  myRndFlag       = false;
  myRnd           = QRandomGenerator::system();
}

Context::~Context() {

  qDebug() << "Context instance is garbage now.";
}

void Context::setPort(QString aPort) {
  myPort = aPort.toUInt();
}

uint Context::getPort() {
  return myPort;
}

void Context::setHost(QString aHost) {
  myHost = aHost;
}

QString Context::getHost() {
  return myHost;
}

void Context::setWaitMS(QString millis) {
  myWaitMS = millis.toUInt();
}

uint Context::getWaitMS() {
  return myWaitMS;
}

void Context::setSleep(QString millis) {

  mySleepTime = millis.toULong();
  qDebug() << "Going to sleep for" << mySleepTime << "ms between message sends.";
}

ulong Context::getSleep() {
  return mySleepTime;
}

void Context::setInput(QString aFilename) {
  myInputFilename = aFilename;
}

bool Context::digestMessages() {

  myMsgIndex = 0;

  // Open the File
  std::ifstream in(myInputFilename.toStdString());
  // Check if object is valid
  if (!in)
    {
      qDebug() << "Cannot open the File : " << myInputFilename;
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

  if (myRndFlag) {
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

void Context::setMsgMax(QString max) {

  myMaxMsgs = max.toInt();
  qDebug() << "Sending no more than" << myMaxMsgs << "messages to host.";
}

void Context::randomize() {

  qDebug() << "Random mode is on.";
  myRndFlag = true;
}
