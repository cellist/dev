#!/bin/sh
rm -f Makefile  hellotr  hellotr_la.qm  main.o
lrelease hellotr_la.ts
qmake
make
./hellotr 
