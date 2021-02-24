#ifndef CLIENTWINDOW_H
#define CLIENTWINDOW_H

#include <QMainWindow>
#include <QTcpSocket>

namespace Ui {
class ClientWindow;
}

class ClientWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit ClientWindow(QWidget *parent = 0);
    ~ClientWindow();

public slots:
    void onReadyRead();

private:
    Ui::ClientWindow *ui;
    QTcpSocket  _socket;
};

#endif // CLIENTWINDOW_H
