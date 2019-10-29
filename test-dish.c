#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <zmq.h>

int main(int argc, char **argv)
{
	int ret = 0;
	void *zctx = NULL;
	void *zsock = NULL;
	zmq_msg_t msg;
	char *str = NULL;
	char buffer[128] = "";

	(void)argc;
	(void)argv;

	zctx = zmq_ctx_new();

	zsock = zmq_socket(zctx, ZMQ_DISH);
	if (zsock == NULL) {
		printf("error: create socket\n");
	}

	ret = zmq_join(zsock, "test");
	if (ret < 0) {
		printf("error: join socket\n");
	}

	ret = zmq_bind(zsock, "udp://*:5555");
	if (ret < 0) {
		printf("error: connect socket\n");
	}

	while (1) {
		zmq_msg_init(&msg);

		ret = zmq_msg_recv(&msg, zsock, 0);
		if (ret < 0) {
			printf("error: recv [%s]\n", zmq_strerror(errno));
			return -1;
		}

		str = zmq_msg_data(&msg);
		memcpy(buffer, str, ret);
		buffer[ret] = '\0';
		printf("recv: %s\n", buffer);

		zmq_msg_close(&msg);
	}

	return 0;
}
