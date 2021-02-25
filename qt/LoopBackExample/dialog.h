#ifndef DIALOG_H
#define DIALOG_H

#include <QDialog>
#include <QTcpServer>
#include <QTcpSocket>
#include <QPushButton>
#include <QLabel>
#include <QProgressBar>
#include <QMessageBox>

#include <log4cplus/logger.h>

namespace Ui {
class Dialog;
}

class Dialog : public QDialog
{
    Q_OBJECT

public:
    explicit Dialog(QWidget *parent = 0);
    ~Dialog();

public slots:
    // start button
    void startListening();

    // request button
    void requestConnection();

    // server accepts a request from a client
    void acceptConnection();

    // client starts sending at the acceptance of a connection request
    void clientSendMessageToServer();

    // slot for server progress bar
    void updateServerProgress();

    // slot for client progress bar
    void updateClientProgress(qint64 numBytes);

    void displayError(QAbstractSocket::SocketError socketError);

private:
    Ui::Dialog *ui;

    QTcpServer tcpServer;
    QTcpSocket tcpClient;
    QTcpSocket *tcpServerConnection;

    log4cplus::Logger logger;
    int bytesToWrite;
    int bytesWritten;
    int bytesReceived;
};

#endif // DIALOG_H
