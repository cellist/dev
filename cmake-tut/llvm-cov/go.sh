#!/bin/sh

# Step 1: Compile with coverage enabled.
clang++ -fprofile-instr-generate -fcoverage-mapping foo.cc -o foo

# Step 2: Run the program.
env LLVM_PROFILE_FILE="foo.profraw" ./foo

# Step 3(a): Index the raw profile.
llvm-profdata merge -sparse foo.profraw -o foo.profdata

# Step 3(b): Create a line-oriented coverage report.
llvm-cov show ./foo -instr-profile=foo.profdata

# Step 3(c): Create a coverage summary.
llvm-cov report ./foo -instr-profile=foo.profdata
