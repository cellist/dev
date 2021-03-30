#include <QtDebug>
#include <stdlib.h>
#include <iostream>

#include "context.h"
#include "client.h"

int main(int argc, char *argv[])
{
  QCoreApplication app(argc, argv);
  QCoreApplication::setApplicationName("Datagrams-over-TCP-socket sender");
  QCoreApplication::setApplicationVersion("1.0");
    
  Context ctx(app, argc, argv);
  Client client;

  client.connectAndSend(ctx);

  std::cin.get();
  return 0;
}
