#!/bin/sh

mkdir -p build &&\
    cd build &&\
    rm -rf * &&\
    env CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake .. &&\
    cmake --build . --config Debug &&\
    cd ..

[ -e ./build/loadcsv ] && ./build/loadcsv input.csv
