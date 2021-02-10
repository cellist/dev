#!/bin/sh

mkdir -p build
cd build &&\
    env CXX=/usr/bin/clang++ cmake .. &&\
    make &&\
    cd .. &&\
    env LLVM_PROFILE_FILE="./build/main_test.profraw" ./build/main_test &&\
    llvm-profdata merge -sparse ./build/main_test.profraw -o ./build/main_test.profdata &&\
    llvm-cov show ./build/main_test -instr-profile=./build/main_test.profdata
