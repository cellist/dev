#include "dialog.h"
#include "ui_dialog.h"

#include <QDebug>

static const int TotalBytes = 50 * 1024 * 1024;
static const int PayloadSize = 64 * 1024; // 64 KB

Dialog::Dialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Dialog)
{
    ui->setupUi(this);

    // request button - initially disabled
    ui->requestButton->setEnabled(false);

    connect(&tcpServer, SIGNAL(newConnection()),
            this, SLOT(acceptConnection()));
    connect(&tcpClient, SIGNAL(connected()),
            this, SLOT(clientSendMessageToServer()));
    connect(&tcpClient, SIGNAL(bytesWritten(qint64)),
            this, SLOT(updateClientProgress(qint64)));
    connect(&tcpClient, SIGNAL(error(QAbstractSocket::SocketError)),
            this, SLOT(displayError(QAbstractSocket::SocketError)));
}

Dialog::~Dialog()
{
    delete ui;
}

// "Start Linstening" button clicked
void Dialog::startListening()
{
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
    tcpClient.connectToHost(QHostAddress::LocalHost, tcpServer.serverPort());
}

// A slot for the newConnection()
void Dialog::acceptConnection()
{
    // nextPendingConnection() to accept the pending connection as a connected QTcpSocket.
    // This function returns a pointer to a QTcpSocket
    tcpServerConnection = tcpServer.nextPendingConnection();

    connect(tcpServerConnection, SIGNAL(readyRead()),
            this, SLOT(updateServerProgress()));
    connect(tcpServerConnection, SIGNAL(error(QAbstractSocket::SocketError)),
            this, SLOT(displayError(QAbstractSocket::SocketError)));

    ui->serverStatusLabel->setText(tr("Accepted connection"));
    tcpServer.close();
}

void Dialog::clientSendMessageToServer()
{
    // called when the TCP client connected to the loopback server
    bytesToWrite = TotalBytes - (int)tcpClient.write(QByteArray(PayloadSize, '@'));
    ui->clientStatusLabel->setText(tr("Connected"));
}

void Dialog::updateServerProgress()
{
    bytesReceived += (int)tcpServerConnection->bytesAvailable();
    tcpServerConnection->readAll();

    ui->serverProgressBar->setMaximum(TotalBytes);
    ui->serverProgressBar->setValue(bytesReceived);
    ui->serverStatusLabel->setText(tr("Received %1MB")
                               .arg(bytesReceived / (1024 * 1024)));

    if (bytesReceived == TotalBytes) {
        tcpServerConnection->close();
        ui->startButton->setEnabled(true);
#ifndef QT_NO_CURSOR
        QApplication::restoreOverrideCursor();
#endif
    }
}

void Dialog::updateClientProgress(qint64 numBytes)
{
    // callen when the TCP client has written some bytes
    bytesWritten += (int)numBytes;

    // only write more if not finished and when the Qt write buffer is below a certain size.
    if (bytesToWrite > 0 && tcpClient.bytesToWrite() <= 4*PayloadSize)
        bytesToWrite -= (int)tcpClient.write(QByteArray(qMin(bytesToWrite, PayloadSize), '@'));

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

    // Calling close() makes QTcpServer stop listening for incoming connections.
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
