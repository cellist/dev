I am assessing the use of cmake for C++ projects at the moment.
This is my first try at level one, so to say (having just one source file).

To build this under Linux you can do:

    mkdir build
    cd build
    cmake ..
    cmake --build .

This will create the *hello-world* executable in the *build* subdirectory.