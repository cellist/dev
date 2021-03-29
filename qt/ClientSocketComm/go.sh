#!/bin/sh

rm -rf build TAGS
etags *.cpp */*.cpp
mkdir -p build &&\
    cd build &&\
    env CXX=/usr/bin/clang++ cmake .. &&\
    cmake --build . &&\
    cd ..

[ -f ./build/clntcomm ] &&\
    ./build/clntcomm -f resources/telegrams.txt -h localhost -m 100 -p 8080 -r -s 10 -w 3000
