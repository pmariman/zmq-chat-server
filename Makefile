all: test-sub test-pub test-dish

LFLAGS=-lzmq -DZMQ_BUILD_DRAFT_API

test-sub: test-sub.c
	gcc -o $@ $^ $(LFLAGS) 

test-pub: test-pub.c
	gcc -o $@ $^ $(LFLAGS) 

test-dish: test-dish.c
	gcc -o $@ $^ $(LFLAGS) 

clean:
	rm -f test-sub test-pub test-dish
