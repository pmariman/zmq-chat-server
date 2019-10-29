apt install vim wget build-essential git python3 python3-pi

export ZMQ_VERSION=4.3.2
export PREFIX=/usr/local

wget https://github.com/zeromq/libzmq/releases/download/v${ZMQ_VERSION}/zeromq-${ZMQ_VERSION}.tar.gz -O libzmq.tar.gz
tar -xzf libzmq.tar.gz
cd zeromq-${ZMQ_VERSION}
./configure --prefix=${PREFIX} --enable-drafts
make -j 8 && make install


pip3 install -v --pre pyzmq --install-option=--enable-drafts --install-option=--zmq=${PREFIX}

