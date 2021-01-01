This is a slightly more advanced example, level 2, so to say ...
Now cmake has to deal with more than one source file.

With this, I am also familiarizing myself with the Standard Template
Library concepts again, after several years of no involvement in any
practical C++ development. I have to confess this is also a recap of
OOP in C++ for me :blush:.

To get this going, do:

    mkdir build
    cd build
    cmake ..
    cmake --build .

You can afterwards also do:

    cd build
	make doxygen
	
now, in case you have [doxygen](https://www.doxygen.nl/index.html) and
the [graphviz](https://graphviz.org/) package installed on your
system.

With the input files provided, you can try:

    ./build/text-analysis fox.txt
	./build/text-analysis
