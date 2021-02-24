#include "client_window.h"
#include "ui_client_window.h"

#include <QDebug>
#include <QHostAddress>

ClientWindow::ClientWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::ClientWindow),
    _socket(this)
{
    ui->setupUi(this);
    _socket.connectToHost(QHostAddress("127.0.0.1"), 4242);
    connect(&_socket, SIGNAL(readyRead()), this, SLOT(onReadyRead()));
}

ClientWindow::~ClientWindow()
{
    delete ui;
}

void ClientWindow::onReadyRead()
{
    QByteArray datas = _socket.readAll();
    qDebug() << datas;
    _socket.write(QByteArray("ok !\n"));
}
