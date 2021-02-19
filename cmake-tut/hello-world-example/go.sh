#!/bin/sh
# Borrowed heavily from https://riptutorial.com/cmake/example/7501/simple--hello-world--project
#
mkdir -p build

cd build &&\
    env CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake .. &&\
    cmake --build .
cd ..

[ -f ./build/hello-world ] && ./build/hello-world
[ -f ./build/check-defines ] && ./build/check-defines
