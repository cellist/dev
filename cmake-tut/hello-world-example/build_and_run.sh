#!/bin/sh
# Borrowed heavily from https://riptutorial.com/cmake/example/7501/simple--hello-world--project
#
mkdir -p build
cd build && cmake .. && cmake --build .
../build/hello-world
