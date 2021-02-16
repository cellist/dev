#!/bin/sh

# Let's try and create a graphical call graph
# from profiling an interactive application ;-)
#
# Requires:
# - exuberant tags (etags, for Emacs, really optional)
# - graphviz (for dot, mandatory)
# - gprof, gprof2dot.py (pip install ...)
#
rm -f gmon.out gmon.dot TAGS
etags *.cpp *.h

mkdir -p build

cd build/ &&\
    env CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake .. &&\
    cmake -DCMAKE_CXX_FLAGS="-pg -fprofile-instr-generate -fcoverage-mapping" \
	  -DCMAKE_BUILD_TYPE=Debug --build . &&\
    make &&\
    env LLVM_PROFILE_FILE="books.profraw" ./books &&\
    gprof -b ./books ./gmon.out |\
	gprof2dot |\
	dot -Tpng -o ./gprof.png &&\
    cd .. &&\
    xli ./build/gprof.png &&\
    llvm-profdata merge -sparse ./build/books.profraw -o ./build/books.profdata &&\
    llvm-cov show ./build/books -instr-profile=./build/books.profdata | xless
