#!/bin/sh

mkdir -p build &&\
    cd build &&\
    rm -rf * &&\
    env CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake .. &&\
    cmake --build . &&\
    cd ..

[ -f ./build/client_server ] && ./build/client_server | head -30
