#ifndef _CONTROLLER_H_
#define _CONTROLLER_H_

#include <QThread>
#include <QString>

class Controller : public QObject
{
  Q_OBJECT
  QThread workerThread;

public:
  Controller();
  ~Controller();
	       
public slots:
  void handleResults(const QString &);
signals:
  void operate(const QString &);
};

#endif // _CONTROLLER_H_
