#!/bin/sh

rm -rf build
mkdir -p build &&\
    cd build &&\
    env CXX=/usr/bin/clang++ cmake .. &&\
    cmake  --build .

cd ..
