#include "dialog.h"
#include "ui_dialog.h"

#include <QDebug>

#include <log4cplus/loglevel.h>
#include <log4cplus/loggingmacros.h>

static const int TotalBytes = 50 * 1024 * 1024;
static const int PayloadSize = 64 * 1024; // 64 KB

Dialog::Dialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Dialog)
{
    this->logger = log4cplus::Logger::getInstance(LOG4CPLUS_TEXT("Dialog"));
    logger.setLogLevel(log4cplus::TRACE_LOG_LEVEL);
    ui->setupUi(this);
    
    // request button - initially disabled
    ui->requestButton->setEnabled(false);

    connect(&tcpServer, SIGNAL(newConnection()),
            this, SLOT(acceptConnection()));
    LOG4CPLUS_INFO(logger,
		   "TcpServer::acceptConnection bound to newConnection().");
    
    connect(&tcpClient, SIGNAL(connected()),
            this, SLOT(clientSendMessageToServer()));
    LOG4CPLUS_INFO(logger,
		   "TcpClient::clientSendMessageToServer bound to connected().");
    
    connect(&tcpClient, SIGNAL(bytesWritten(qint64)),
            this, SLOT(updateClientProgress(qint64)));
    LOG4CPLUS_INFO(logger,
		   "TcpClient::updateClientProgress bound to bytesWritten().");
    
    connect(&tcpClient, SIGNAL(error(QAbstractSocket::SocketError)),
            this, SLOT(displayError(QAbstractSocket::SocketError)));
    LOG4CPLUS_INFO(logger,
		   "TcpClient::displayError bound to error().");
}

Dialog::~Dialog()
{
    delete ui;
}

// "Start Listening" button clicked
void Dialog::startListening()
{
  LOG4CPLUS_INFO(logger, "TcpServer starts listening.");
  
  ui->startButton->setEnabled(false);
  
  bytesWritten = 0;
  bytesReceived = 0;
  
  while (!tcpServer.isListening() && !tcpServer.listen()) {
    QMessageBox::StandardButton ret = QMessageBox::critical(this,
							    tr("Loopback"),
							    tr("Unable to start the test: %1.")
							    .arg(tcpServer.errorString()),
							    QMessageBox::Retry
							    | QMessageBox::Cancel);
    if (ret == QMessageBox::Cancel)
      return;
  }
  
  ui->serverStatusLabel->setText(tr("Listening"));
  ui->requestButton->setEnabled(true);
}

void Dialog::requestConnection()
{
  ui->requestButton->setEnabled(false);
  ui->clientStatusLabel->setText(tr("Connecting"));
  LOG4CPLUS_INFO(logger, "TcpClient requests connection.");
  tcpClient.connectToHost(QHostAddress::LocalHost, tcpServer.serverPort());
}

// A slot for the newConnection()
void Dialog::acceptConnection()
{
  // nextPendingConnection() to accept the pending connection as a connected QTcpSocket.
  // This function returns a pointer to a QTcpSocket
  tcpServerConnection = tcpServer.nextPendingConnection();
  LOG4CPLUS_INFO(logger, "Next pending connection requested from TcpServer.");
  
  connect(tcpServerConnection, SIGNAL(readyRead()),
	  this, SLOT(updateServerProgress()));
  LOG4CPLUS_INFO(logger,
		 "TcpServerConnection::updateServerProgress bound to readyRead().");
  
  connect(tcpServerConnection, SIGNAL(error(QAbstractSocket::SocketError)),
	  this, SLOT(displayError(QAbstractSocket::SocketError)));
  LOG4CPLUS_INFO(logger,
		 "TcpServerConnection::displayError bound to error().");
  
  ui->serverStatusLabel->setText(tr("Accepted connection"));
  tcpServer.close();
}

void Dialog::clientSendMessageToServer()
{
  char buf[200];
  // called when the TCP client connected to the loopback server
  LOG4CPLUS_INFO(logger, "TcpClient connected to TcpServer.");
  bytesToWrite = TotalBytes - (int)tcpClient.write(QByteArray(PayloadSize, '@'));
  sprintf(buf,
	  "TcpClient writes to server - totalBytes: %d, bytesToWrite: %d, payloadSize: %d.",
	  TotalBytes,
	  bytesToWrite,
	  PayloadSize
	  );
  LOG4CPLUS_INFO(logger, buf);
  ui->clientStatusLabel->setText(tr("Connected"));
}

void Dialog::updateServerProgress()
{
  char buf[200];
  LOG4CPLUS_TRACE(logger, "TcpServer is ready to read.");
  bytesReceived += (int)tcpServerConnection->bytesAvailable();
  tcpServerConnection->readAll();
  sprintf(buf, "TcpServerConnection received %d bytes", bytesReceived);
  LOG4CPLUS_TRACE(logger, buf);
  
  ui->serverProgressBar->setMaximum(TotalBytes);
  ui->serverProgressBar->setValue(bytesReceived);
  ui->serverStatusLabel->setText(tr("Received %1MB")
				 .arg(bytesReceived / (1024 * 1024)));
  
  if (bytesReceived == TotalBytes) {
    sprintf(buf,
	    "TcpServerConnection received %d bytes. Closing.",
	    TotalBytes);
    LOG4CPLUS_TRACE(logger, buf);
    tcpServerConnection->close();
    ui->startButton->setEnabled(true);
#ifndef QT_NO_CURSOR
    QApplication::restoreOverrideCursor();
#endif
  }
}

void Dialog::updateClientProgress(qint64 numBytes)
{
  char buf[200];
  // called when the TCP client has written some bytes
  bytesWritten += (int)numBytes;
  sprintf(buf,
	  "TcpClient wrote %d bytes, totalling %d bytes",
	  (int)numBytes, bytesWritten);
  LOG4CPLUS_TRACE(logger, buf);
  
  // only write more if not finished and when the Qt write buffer is below a certain size.
  if (bytesToWrite > 0 && tcpClient.bytesToWrite() <= 4*PayloadSize) {
    bytesToWrite -= (int)tcpClient.write(QByteArray(qMin(bytesToWrite, PayloadSize), '@'));
    sprintf(buf, "TcpClient still has %d bytes to write.", bytesToWrite);
    LOG4CPLUS_TRACE(logger, buf);
  }
  
  ui->clientProgressBar->setMaximum(TotalBytes);
  ui->clientProgressBar->setValue(bytesWritten);
  ui->clientStatusLabel->setText(tr("Sent %1MB")
				 .arg(bytesWritten / (1024 * 1024)));
}

void Dialog::displayError(QAbstractSocket::SocketError socketError)
{
  if (socketError == QTcpSocket::RemoteHostClosedError)
    return;
  
  QMessageBox::information(this, tr("Network error"),
			   tr("The following error occurred: %1.")
			   .arg(tcpClient.errorString()));
  
  tcpClient.close();
  LOG4CPLUS_INFO(logger, "TcpClient closes down.");
  
  // Calling close() makes QTcpServer stop listening for incoming connections.
  LOG4CPLUS_INFO(logger, "TcpServer closes down.");
  tcpServer.close();
  
  ui->clientProgressBar->reset();
  ui->serverProgressBar->reset();
  ui->clientStatusLabel->setText(tr("Client ready"));
  ui->serverStatusLabel->setText(tr("Server ready"));
  ui->startButton->setEnabled(true);
  ui->requestButton->setEnabled(false);
#ifndef QT_NO_CURSOR
  QApplication::restoreOverrideCursor();
#endif
}
