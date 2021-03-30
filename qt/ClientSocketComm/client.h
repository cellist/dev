#ifndef _CLIENT_H_
#define _CLIENT_H_

#include <QObject>
#include <QString>
#include <QTcpSocket>
#include "context.h"

class Client : public QObject
{
  Q_OBJECT
public:
  Client();
  ~Client();

  void connectAndSend(Context& ctx);

private:
  void sendMessages(Context& ctx);
  void sendAndDisengage(QString& host, Context& ctx);

  uint        myPort;
  QString     myHost;
  QTcpSocket* mySocket;
};
#endif /* _CLIENT_H_ */
