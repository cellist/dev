#!/bin/sh

rm -rf build TAGS
etags *.cpp
mkdir -p build &&\
    cd build &&\
    env CXX=/usr/bin/clang++ cmake .. &&\
    cmake --build . &&\
    cd ..
[ -f ./build/signal-slot ] && ./build/signal-slot

