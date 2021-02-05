#!/bin/sh

# Create an executable with debugging information
# and create a run-time profile report
#

mkdir -p build
cd build &&\
    cmake  -DCMAKE_CXX_FLAGS=-pg -DCMAKE_BUILD_TYPE=Debug .. &&\
    make &&\
    file hello-world &&\
    ./hello-world &&\
    gprof ./hello-world gmon.out | less
