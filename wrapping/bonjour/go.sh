#!/bin/sh

mkdir -p build

cd build &&\
    env CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake .. &&\
    cmake  --build . &&\
    ldd pylib.so &&\
    env PYTHONPATH=$PYTHONPATH:$PWD ../bonjour.py

cd ..
