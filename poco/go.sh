#!/bin/sh

rm -rf build TAGS
etags *.cc
mkdir -p build &&\
    cd build &&\
    env CXX=/usr/bin/clang++ cmake .. &&\
    cmake --build . &&\
    cd ..

[ -f ./build/pocothreads ] && ./build/pocothreads
[ -f ./build/pocoevents ] && ./build/pocoevents
[ -f ./build/pocoactive ] && ./build/pocoactive
[ -f ./build/pocohttptime ] && ./build/pocohttptime -h
