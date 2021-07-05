#!/bin/sh

mkdir -p build &&\
    cd build &&\
    rm -rf * &&\
    env CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake .. &&\
    cmake --build . --config Debug &&\
    cd ..

[ -f ./build/simple_example_2 ] && ./build/simple_example_2
