#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <zmq.h>


int main(int argc, char **argv)
{
	int ret = 0;
	void *zctx = NULL;
	void *zsock = NULL;
	char msg[128] = "";

	(void)argc;
	(void)argv;

	zctx = zmq_ctx_new();

	zsock = zmq_socket(zctx, ZMQ_SUB);

	ret = zmq_connect(zsock, "tcp://172.17.0.3:5555");
	if (ret < 0) {
		printf("error: connect socket\n");
	}

	ret = zmq_setsockopt(zsock, ZMQ_SUBSCRIBE, "test:", 5);
	if (ret < 0) {
		printf("error: connect subscribe\n");
	}

	while (1) {
		ret = zmq_recv(zsock, msg, 128, 0);
		if (ret <= 0) {
			printf("error: recv\n");
		} else {
			msg[ret] = '\0';
			printf("recv: %s\n", msg);
		}
	}

	return 0;
}
