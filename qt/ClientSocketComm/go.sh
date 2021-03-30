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
	-H 127.0.0.1 \
	-I resources/telegrams.txt \
	-M 100 \
	-P 8080 \
	-R \
	-S 10 \
	-W 3000
