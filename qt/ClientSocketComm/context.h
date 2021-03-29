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

  void setPort(quint16 aPort);
  quint16 getPort();

  void setHost(char* aHost);
  QString getHost();

  void setWaitMS(quint16 millis);
  quint16 getWaitMS();

  void setSleep(quint16 millis);
  unsigned long getSleep();

  void setInput(char* aFilename);
  bool getNextMessage(std::string& msg);
  quint16 getMsgIndex();
  void setMsgMax(quint16 max);

  void randomize();

private:
  bool digestMessages();

  quint16                  myPort;
  QString                  myHost;
  quint16                  myWaitMS;
  std::string              myInputFilename;
  std::vector<std::string> myMsgs;
  int                      myMsgIndex;
  unsigned long            mySleepTime;
  bool                     myRndFlag;
  quint16                  myMaxMsgs;
  QRandomGenerator        *myRnd;
};

#endif // _CONTEXT_H_
