#ifndef _CONTEXT_H_
#define _CONTEXT_H_

#include <string>
#include <vector>
#include <QObject>
#include <QString>
#include <QCoreApplication>
#include <QRandomGenerator>

class Context : public QObject {
  Q_OBJECT
public:
  Context(QCoreApplication& app, int argc, char* argv[]);
  ~Context();

  uint    getPort();
  QString getHost();
  uint    getWaitMS();
  ulong   getSleep();
  bool    getNextMessage(std::string& msg);
  uint    getMsgIndex();

private:
  bool digestMessages();
  void processArgs(QCoreApplication& app, int argc, char* argv[]);
  
  uint                     myPort;
  QString                  myHost;
  uint                     myWaitMS;
  QString                  myInputFilename;
  std::vector<std::string> myMsgs;
  uint                     myMsgIndex;
  ulong                    mySleepTime;
  uint                     myMaxMsgs;
  QRandomGenerator*        myRnd;
};

#endif // _CONTEXT_H_
