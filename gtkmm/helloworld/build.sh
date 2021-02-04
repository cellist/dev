#!/bin/sh
mkdir -p build &&\
 cd build &&\
 cmake .. &&\
 cmake --build . &&\
 cd .. &&\
 /usr/bin/printf "You may want to try\n\n\t./build/gtkmm_hello_world\n\nnow ;-)\n"


