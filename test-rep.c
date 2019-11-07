#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <zmq.h>


int main(int argc, char **argv)
{
	int ret = 0;
    int cnt = 1;
	void *zctx = NULL;
	void *zsock = NULL;
	char msg[128] = "";

	zctx = zmq_ctx_new();

	zsock = zmq_socket(zctx, ZMQ_REP);

    // server ip = 10.32.10.160
	ret = zmq_bind(zsock, "tcp://0.0.0.0:5555");
	if (ret < 0) {
		printf("error: bind socket\n");
	}

	while (1) {
		ret = zmq_recv(zsock, msg, 127, 0);
		if (ret < 0) {
			printf("error: recv\n");
            return -1;
		}

        msg[ret] = '\0';
        printf(">>> [%d] [%s]\n", cnt, msg);

        snprintf(msg, 128, "place %d\n", cnt);

        ret = zmq_send(zsock, msg, strlen(msg), 0);
		if (ret < 0) {
			printf("error: send\n");
            return -1;
		}

        cnt++;
	}

	return 0;
}
