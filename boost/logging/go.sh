#!/bin/sh

mkdir -p build &&\
    cd build &&\
    rm -rf * &&\
    env CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake .. &&\
    cmake --build . --config Debug &&\
    cd ..

[ -f ./build/mem_leak ] && valgrind --leak-check=full ./build/mem_leak
[ -f ./build/no_leak ]  && valgrind --leak-check=full ./build/no_leak
