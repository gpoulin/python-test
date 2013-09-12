SHELL = /bin/sh
CC    = gcc
CFLAGS       = -fPIC -march=native -mtune=native -O3
LDFLAGS      = -shared

TARGET  = ctype.so
SOURCES = ctype.c
OBJECTS = $(SOURCES:.c=.o)

PREFIX = $(DESTDIR)/usr/local
BINDIR = $(PREFIX)/bin

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(TARGET) $(OBJECTS)
