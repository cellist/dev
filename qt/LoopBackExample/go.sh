#!/bin/sh

rm -rf build TAGS
etags *.cpp
mkdir -p build &&\
    cd build &&\
    env CXX=/usr/bin/clang++ cmake .. &&\
    cmake -DCODE_COVERAGE=ON --build . &&\
    make &&\
    cd .. &&\
    env LLVM_PROFILE_FILE="./build/my.profraw" ./build/loopback-example &&\
    llvm-profdata merge -sparse ./build/my.profraw -o ./build/my.profdata &&\
    llvm-cov show ./build/loopback-example -instr-profile=./build/my.profdata

