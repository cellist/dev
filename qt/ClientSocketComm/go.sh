#!/bin/sh

rm -rf build TAGS
etags *.cpp
mkdir -p build &&\
    cd build &&\
    env CXX=/usr/bin/clang++ cmake .. &&\
    cmake --build . &&\
    cd ..

[ -f ./build/clntcomm ] &&\
    ./build/clntcomm \
	--host 127.0.0.1 \
	--input-file resources/telegrams.txt \
	--max-messages 100 \
	--port 8080 \
	--randomize \
	--sleep-between-sends 10 \
	--wait 3000
