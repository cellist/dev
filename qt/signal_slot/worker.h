#ifndef _WORKER_H_
#define _WORKER_H_

#include <QObject>
#include <QString>

class Worker : public QObject
{
  Q_OBJECT
  
public slots:
  void doWork(const QString &parameter);
  
signals:
  void resultReady(const QString &result);
};

#endif // _WORKER_H_
