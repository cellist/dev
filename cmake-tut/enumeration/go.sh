#!/bin/sh
#
rm -rf build && mkdir -p build

cd build &&\
    env CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake .. &&\
    cmake -DCMAKE_CXX_FLAGS="-pg -fprofile-instr-generate -fcoverage-mapping" -DCMAKE_BUILD_TYPE=Debug --build . &&\
    make
cd ..

[ -f ./build/enumeration ] &&\
    env LLVM_PROFILE_FILE="./build/enumeration.profraw" ./build/enumeration
