#include <unistd.h>
#include <QDebug>

#include "worker.h"

void Worker::doWork(const QString &parameter) {

  qDebug() << "Worker thread commences work.";
  QString result = QString::number(sleep(3));
  
  qDebug() << "Worker thread done, sending result ready signal, result is: "
	   << result;
  emit resultReady(result);
}
