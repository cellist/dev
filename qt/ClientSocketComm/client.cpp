#include "client.h"
#include <stdlib.h>
#include <QThread>
#include <QtDebug>

Client::Client() {

  mySocket = new QTcpSocket(this);
  qDebug() << "Initialized client with TCP socket";
}


Client::~Client()
{
  qDebug() << "Client is garbage now.";
}

void Client::connectAndSend(Context& ctx)
{
  QString host = ctx.getHost();
  quint16 port = ctx.getPort();
  quint16 millis = ctx.getWaitMS();

  qDebug() << "Trying to connect to " << host << ":" << port;

  mySocket->connectToHost(host, port);

  if (mySocket->waitForConnected(millis)) {
    qDebug() << "Connected to " << host << ":" << port;

    this->sendMessages(ctx);
    mySocket->close();
    qDebug() << "Disconnected.";

  } else {
    qDebug() << "Connection timed out!";
  }
}

void Client::sendMessages(Context& ctx) {

  quint16 millis = ctx.getWaitMS();
  unsigned long sleepTime = ctx.getSleep();
  unsigned int msgCount = 0;

  std::string msg;

  while (ctx.getNextMessage(msg)) {
    mySocket->write(msg.c_str());
    qDebug() << "Sending " << msg.size() << "bytes from message index" << ctx.getMsgIndex() << ".";
    mySocket->waitForBytesWritten(millis);
    qDebug() << "Message" << ++msgCount << "transferred.";

    // qDebug() << "Reading" << mySocket->bytesAvailable() << "bytes.";
    mySocket->readAll();

    if(sleepTime > 0) {
      QThread::msleep(sleepTime);
    }
  }
}
