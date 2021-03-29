#include <QtDebug>
#include <stdlib.h>
#include <iostream>
#include "getopt.h"

#include "context.h"
#include "client.h"

int main(int argc, char *argv[])
{
	Context ctx;
	Client client;

	int opt;
	char buf[30];

	/*
	** -f <file>: take messages from <file>, default: msg.txt
	** -h <host>: host to connect to, default: localhost
	** -m <max>:  send at most <max> messages in total, default: 10000 (0: no limit)
	** -p <port>: port for the connection, default: 8080
	** -r: send messages randomly, default: line by line from top to bottom;
	** -s <msec>: sleep for <msec> ms between message sends, default: 0 (no waiting at all)
	** -w <msec>: wait for response with a maximum of <msec> ms before timing out, default: 5000
	*/
	while ((opt = getopt(argc, argv, "f:h:m:p:rs:w:")) != -1)
		switch (opt) {
		case 'f':
			ctx.setInput(optarg);
			break;
		case 'h':
			ctx.setHost(optarg);
			break;
		case 'm':
			ctx.setMsgMax(atoi(optarg));
			break;
		case 'p':
			ctx.setPort(atoi(optarg));
			break;
		case 'r':
			ctx.randomize();
			break;
		case 's':
			ctx.setSleep(atoi(optarg));
			break;
		case 'w':
			ctx.setWaitMS(atoi(optarg));
			break;
		default:
			sprintf(buf, "Unknown option: %c", opt);
			qDebug() << buf;
		}

	client.connectAndSend(ctx);

	std::cin.get();
	return 0;
}
