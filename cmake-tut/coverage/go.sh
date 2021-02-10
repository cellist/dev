#!/bin/sh

mkdir -p build
cd build &&\
    env CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake .. &&\
    cmake -DCODE_COVERAGE=ON --build . &&\
    make &&\
    cd .. &&\
    env LLVM_PROFILE_FILE="./build/coverage.profraw" ./build/coverage &&\
    llvm-profdata merge -sparse ./build/coverage.profraw -o ./build/coverage.profdata &&\
    llvm-cov show ./build/coverage -instr-profile=./build/coverage.profdata
