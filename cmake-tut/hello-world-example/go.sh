#!/bin/sh
# Borrowed heavily from https://riptutorial.com/cmake/example/7501/simple--hello-world--project
#
rm -rf build && mkdir -p build

cd build &&\
    env CC=/usr/bin/clang CXX=/usr/bin/clang++ cmake .. &&\
    cmake -DCMAKE_CXX_FLAGS="-pg -fprofile-instr-generate -fcoverage-mapping" -DCMAKE_BUILD_TYPE=Debug --build . &&\
    make
cd ..

[ -f ./build/hello-world ] &&\
    env LLVM_PROFILE_FILE="./build/hello-world.profraw" ./build/hello-world

[ -f ./build/check-defines ] &&\
    env LLVM_PROFILE_FILE="./build/check-defines.profraw" ./build/check-defines &&\
    llvm-profdata merge -sparse ./build/check-defines.profraw -o ./build/check-defines.profdata &&\
    llvm-cov show ./build/check-defines -instr-profile=./build/check-defines.profdata | xless

# Ask preprocessor about known macros
# echo | cpp -dM | sort -u

[ -f ./build/cli_param ] &&\
    env LLVM_PROFILE_FILE="./build/cli_param.profraw" \
	./build/cli_param --add --append --create create_this \
	--delete delete_this --file some_file --verbose --help \
	hello, world &&\
    llvm-profdata merge -sparse ./build/cli_param.profraw -o ./build/cli_param.profdata &&\
    llvm-cov show ./build/cli_param -instr-profile=./build/cli_param.profdata
