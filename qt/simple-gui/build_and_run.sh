#!/bin/sh

mkdir -p build &&\
    cd build &&\
    cmake .. &&\
    cmake --build . &&\
    cd .. &&\
    file ./build/simple-gui &&\
    ./build/simple-gui
