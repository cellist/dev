#include <iostream>
#include <iterator>
#include <fstream>
#include <algorithm> // for std::copy
#include <QtDebug>
#include "context.h"

Context::Context() {

	/* Set default values */
	myHost = "localhost";
	myPort = 8080;
	myWaitMS = 5000;
	myInputFilename = "msg.txt";
	mySleepTime = 0;
	myMaxMsgs = 0;
	myRndFlag = false;
	myRnd = QRandomGenerator::system();
}

Context::~Context() {

	qDebug() << "Context instance is garbage now.";
}

void Context::setPort(quint16 aPort) {
	myPort = aPort;
}

quint16 Context::getPort() {
	return myPort;
}

void Context::setHost(char* aHost) {
	myHost = aHost;
}

QString Context::getHost() {
	return myHost;
}

void Context::setWaitMS(quint16 millis) {
	myWaitMS = millis;
}

quint16 Context::getWaitMS() {
	return myWaitMS;
}

void Context::setSleep(quint16 millis) {

	qDebug() << "Going to sleep for " << millis << "ms between message sends.";
	mySleepTime = millis;
}

unsigned long Context::getSleep() {
	return mySleepTime;
}

void Context::setInput(char* aFilename) {
	myInputFilename = aFilename;
}

bool Context::digestMessages() {

	myMsgIndex = 0;

	// Open the File
	std::ifstream in(myInputFilename.c_str());
	// Check if object is valid
	if (!in)
	{
		qDebug() << "Cannot open the File : " << myInputFilename.c_str();
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

quint16 Context::getMsgIndex() {

	return myMsgIndex;
}

void Context::setMsgMax(quint16 max) {

	qDebug() << "Sending no more than " << max << " messages to host.";
	myMaxMsgs = max;
}

void Context::randomize() {

	qDebug() << "Random mode is on.";
	myRndFlag = true;
}