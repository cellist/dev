#include <log4cplus/configurator.h>

#include "dialog.h"
#include <QApplication>

int main(int argc, char *argv[])
{
  log4cplus::BasicConfigurator config;
  config.configure();

  QApplication a(argc, argv);
  Dialog w;
  w.setWindowTitle("Loopback Dialog Example");
  w.show();
  
  return a.exec();
}
