#include "client.h"
#include <stdlib.h>
#include <QHostInfo>
#include <QThread>
#include <QtDebug>

Client::Client() {

  mySocket = new QTcpSocket(this);
  qDebug() << "Initialized client with TCP socket.";
}

Client::~Client()
{
  qWarning() << "Client is garbage now.";
}

void Client::sendAndDisengage(QString& host, Context& ctx) {

  uint port = ctx.getPort();
  
  qDebug() << "Connected to " << host << ":" << port << ".";
  
  this->sendMessages(ctx);
  mySocket->close();
  qDebug() << "Disconnected from " << host << ".";
}
  
void Client::connectAndSend(Context& ctx)
{
  QString host = ctx.getHost();
  uint port    = ctx.getPort();
  uint millis  = ctx.getWaitMS();
  
  qDebug() << "Trying to connect to " << host << ":" << port << ".";
  mySocket->connectToHost(host, port);

  if (mySocket->waitForConnected(millis)) {
    this->sendAndDisengage(host, ctx);
  } else {
    QHostInfo lookup = QHostInfo::fromName(host);
    host = lookup.hostName();
    qWarning() << "Connection timed out! Trying DNS lookup.";

    if(lookup.error() != QHostInfo::NoError) {
      qWarning() << "The hostname DNS lookup has failed or IP address is invalid.";
      return;
    }

    qDebug() << "Trying to connect to " << host << ":" << port << "now.";
    mySocket->connectToHost(host, port);

    if (mySocket->waitForConnected(millis)) {
      this->sendAndDisengage(host, ctx);
    } else {
      qWarning() << "Connection timed out as well!";
    }
  }
}

void Client::sendMessages(Context& ctx) {

  uint millis = ctx.getWaitMS();
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
