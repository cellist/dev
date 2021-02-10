#!/bin/sh

mkdir -p build
cd build && env CXX=clang++ cmake .. && make && cd .. &&\
    ./build/main_test
