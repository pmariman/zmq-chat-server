#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <zmq.h>


int main(int argc, char **argv)
{
	int ret = 0;
	void *zctx = NULL;
	void *zsock = NULL;
	char msg[128] = "test:hello";

	zctx = zmq_ctx_new();

	zsock = zmq_socket(zctx, ZMQ_PUB);

	ret = zmq_bind(zsock, "tcp://0.0.0.0:5555");
	if (ret < 0) {
		printf("error: bind socket\n");
	}

	while (1) {
		sleep(1);
		ret = zmq_send(zsock, msg, strlen(msg), 0);
		if (ret != strlen(msg)) {
			printf("error: send\n");
		}
	}

	return 0;
}
