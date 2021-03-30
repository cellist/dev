#ifndef _CONTEXT_H_
#define _CONTEXT_H_

#include <string>
#include <vector>
#include <QObject>
#include <QString>
#include <QRandomGenerator>

class Context : public QObject {
  Q_OBJECT
public:
  Context();
  ~Context();

  void setPort(QString aPort);
  uint getPort();

  void setHost(QString aHost);
  QString getHost();

  void setWaitMS(QString millis);
  uint getWaitMS();

  void setSleep(QString millis);
  ulong getSleep();

  void setInput(QString aFilename);
  bool getNextMessage(std::string& msg);
  uint getMsgIndex();
  void setMsgMax(QString max);

  void randomize();

private:
  bool digestMessages();

  uint                     myPort;
  QString                  myHost;
  uint                     myWaitMS;
  QString                  myInputFilename;
  std::vector<std::string> myMsgs;
  uint                     myMsgIndex;
  ulong                    mySleepTime;
  bool                     myRndFlag;
  uint                     myMaxMsgs;
  QRandomGenerator        *myRnd;
};

#endif // _CONTEXT_H_
