#!/bin/sh

rm -rf build TAGS
etags *.cpp */*.cpp
mkdir -p build &&\
    cd build &&\
    env CXX=/usr/bin/clang++ cmake .. &&\
    cmake --build . &&\
    cd ..

# [ -f ./build/ncgui ] && ./build/ncgui
[ -f ./build/ncgui ] && valgrind --leak-check=full ./build/ncgui 2>&1 |\
    less
								      

