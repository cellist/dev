#!/bin/sh

mkdir -p build
cd build && cmake .. &&\
    cmake --build .&&\
    cat -n ../memoryLeak.c &&\
    valgrind --leak-check=full ./memoryLeak &&\
    cat -n ../simpleOptions.c &&\
    valgrind --leak-check=full ./simpleOptions --db mydb --ignore ignore_this
