#include <unistd.h>
#include <QDebug>
#include <QCoreApplication>

#include "controller.h"
#include "worker.h"

Controller::Controller() {
  Worker *worker = new Worker;
  worker->moveToThread(&workerThread);
  connect(&workerThread, &QThread::finished, worker, &QObject::deleteLater);
  connect(this, &Controller::operate, worker, &Worker::doWork);
  connect(worker, &Worker::resultReady, this, &Controller::handleResults);
  qDebug() << "Worker thread built and signal connected.";
  workerThread.start();
  qDebug() << "Worker thread started.";
}

Controller::~Controller() {
  qDebug() << "About to do workerThread.quit().";
  workerThread.quit();
  qDebug() << "About to do workerThread.wait().";
  workerThread.wait();
}

void Controller::handleResults(const QString &result) {
  qDebug() << "Worker thread finished. Result is: " << result;
}

int main(int argc, char* argv[]) {
  QCoreApplication app(argc, argv);
  Controller ctrl;

  return app.exec();
}
