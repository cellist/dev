#ifndef _client_h_
#define _client_h_

#include <QtCore>
#include <QtNetwork>

class Client : public QObject
{
    Q_OBJECT
public:
    explicit Client(QObject *parent = 0);

public slots:
    bool connectToHost(QString host);
    bool writeData(QByteArray data);

private:
    QTcpSocket *socket;
};

#endif // _client_h_
