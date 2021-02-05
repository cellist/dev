#!/bin/sh

mkdir -p build
cd build && cmake .. &&\
    cmake --build .&&\
    cat -n ../memoryLeak.c &&\
    valgrind --leak-check=full ./memoryLeak
