#ifndef SERVER_WINDOW_H
#define SERVER_WINDOW_H

#include <QMainWindow>
#include <QTcpServer>
#include <QTcpSocket>

namespace Ui {
class ServerWindow;
}

class ServerWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit ServerWindow(QWidget *parent = 0);
    ~ServerWindow();

public slots:
    void onNewConnection();
    void onSocketStateChanged(QAbstractSocket::SocketState socketState);
    void onReadyRead();
private:
    Ui::ServerWindow *ui;
    QTcpServer  _server;
    QList<QTcpSocket*>  _sockets;
};

#endif // SERVER_WINDOW_H
