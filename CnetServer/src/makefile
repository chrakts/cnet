IDIR = /usr/local/include
CC=g++

CPPFLAGS=-I$(IDIR) -Wall -g -std=c++11 -O3 -o CnetServer -rdynamic -D_GNU_SOURCE

ODIR=.
LDIR =/usr/local/lib . 

LIBS=libcrc.a -lstdc++ -lserial -llcm -lm

_DEPS = argparse.h checksum.h CNET.h CNETLCMHDL.h cnet_answer_t.hpp cnet_command_t.hpp cnet_constants_t.hpp cnet_crc_constants_t.hpp lcm_cnet.hpp
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ =  argparse.o CNET.o CNETLCMHDL.o CnetServer.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))


$(ODIR)/%.o: %.cpp $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

CnetServer: $(OBJ)
	g++ -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~ 