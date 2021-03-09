#!/bin/sh

rm -rf build TAGS
etags *.cpp
mkdir -p build &&\
    cd build &&\
    env CXX=/usr/bin/clang++ cmake .. &&\
    cmake --build . &&\
    cd ..

[ -f ./build/client_server ] && ./build/client_server

