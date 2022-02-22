#!/bin/sh
rm -f Makefile  hellotr  hellotr_la.qm  main.o hellotr_la.ts
lupdate hellotr.pro 
# simulate translation work in Qt Linguist through sed
sed -i -e 's# type="unfinished">#>Orbis, te saluto!#' hellotr_la.ts
lrelease hellotr_la.ts
qmake
make
./hellotr 
