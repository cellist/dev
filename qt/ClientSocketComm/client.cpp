#include "client.h"
#include <stdlib.h>
#include <QDateTime>
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
  
void Client::connectAndSend(Context& ctx)
{
  uint millis  = ctx.getWaitMS();
  
  myHost = ctx.getHost();
  myPort = ctx.getPort();
  qDebug() << "Trying to connect to " << myHost << ":" << myPort << ".";
  mySocket->connectToHost(myHost, myPort);

  if(mySocket->waitForConnected(millis)) {
    qDebug() << "Connected to " << myHost << ":" << myPort << ".";
    this->sendMessages(ctx);
    qDebug() << "Finally disconnected from " << myHost << ".";
  } else {
    QHostInfo lookup = QHostInfo::fromName(myHost);
    myHost = lookup.hostName();
    qWarning() << "Connection timed out! Trying DNS lookup.";

    if(lookup.error() != QHostInfo::NoError) {
      qWarning() << "The hostname DNS lookup has failed or IP address is invalid.";
      return;
    }

    qDebug() << "Trying to connect to " << myHost << ":" << myPort << "now.";
    mySocket->connectToHost(myHost, myPort);

    if(mySocket->waitForConnected(millis)) {
      qDebug() << "Connected to " << myHost << ":" << myPort << ".";
      this->sendMessages(ctx);
      qDebug() << "Finally disconnected from " << myHost << ".";
    } else {
      qWarning() << "Connection timed out as well!";
    }
  }
}

void Client::sendMessages(Context& ctx) {

  uint          millis = ctx.getWaitMS();
  unsigned long sleepTime = ctx.getSleep();
  unsigned int  msgCount = 0;
  unsigned int  totalBytes = 0;
  std::string   msg;
  bool          stayConnected = ctx.keepSocketOpen();
  char          buf[100];
  QDateTime     now = QDateTime::currentDateTime();
  qint64        deltaS;
  
  qDebug() << "Socket connection will"
	   << (stayConnected ? "not" : "")
	   << "be closed between transmissions.";
    
  while (ctx.getNextMessage(msg)) {
    mySocket->write(msg.c_str());
    totalBytes += msg.size();
    sprintf(buf,
	    "Sending %lu bytes from message index %d, total: %.1fkB.",
	    msg.size(),
	    ctx.getMsgIndex(),
	    totalBytes/1024.0);
    qDebug() << buf;
    
    mySocket->waitForBytesWritten(millis);
    qDebug() << "Message" << ++msgCount << "transferred.";
    mySocket->readAll();

    if(!stayConnected) {
      mySocket->close();
    }
    
    if(sleepTime > 0) {
      QThread::msleep(sleepTime);
    }

    if(!stayConnected) {
      /* Reconnect for subsequent transmission */
      mySocket->connectToHost(myHost, myPort);
      
      if(!mySocket->waitForConnected(millis)) {
	qWarning() << "Cannot reconnect to " << myHost
		   << " ! Transmission aborted.";
	return;
      } else {
	qDebug() << "Reconnected successfully.";
      }
    }
  }
  deltaS = now.secsTo(QDateTime::currentDateTime());
  if(deltaS > 0) {
    sprintf(buf,
	    "Transmitted %dkB in %lds [%.2fkB/s].",
	    totalBytes/1024,
	    (long)deltaS,
	    totalBytes/1024.0/deltaS);
    qDebug() << buf;
  }
  mySocket->close();
}
