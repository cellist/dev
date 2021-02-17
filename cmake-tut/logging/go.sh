#!/bin/sh

mkdir -p build

cd build &&\
    env CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake .. &&\
    cmake  --build . &&\
    ./simple_logging &&\
    ./advanced_logging

cd ..
