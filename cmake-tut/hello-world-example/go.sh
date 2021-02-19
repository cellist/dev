#!/bin/sh
# Borrowed heavily from https://riptutorial.com/cmake/example/7501/simple--hello-world--project
#
rm -rf build && mkdir -p build

cd build &&\
    env CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake .. &&\
    cmake -DCMAKE_CXX_FLAGS="-pg -fprofile-instr-generate -fcoverage-mapping" -DCMAKE_BUILD_TYPE=Debug --build . &&\
    make
cd ..

[ -f ./build/hello-world ] && ./build/hello-world

[ -f ./build/check-defines ] &&\
    env LLVM_PROFILE_FILE="./build/check-defines.profraw" ./build/check-defines &&\
    llvm-profdata merge -sparse ./build/check-defines.profraw -o ./build/check-defines.profdata &&\
    llvm-cov show ./build/check-defines -instr-profile=./build/check-defines.profdata | xless

# Ask preprocessor about known macros
# echo | cpp -dM | sort -u
