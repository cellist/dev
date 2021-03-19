/*
 * C++ example with a memory leak in an exception
 */
 
#include <iostream>
 
void throwErrorWithMemLeak()
{
    try
    {
        // Allocate 1kB buffer
        char *buffer = new char[1024];
 
        // Throw
        throw 1;
 
        // Free up buffer
        delete[] buffer;
    }
    catch(const int e)
    {
      // std::cout << "We have a memory leak!" << std::endl;
    }
}
 
int main(int args, char **argc)
{
    // A simple case of when an exception leads to a memory leak
 
    // Iterate the throwing function 1024 times, creating a 1MB memeory leak
    for (size_t i = 0; i < 1024; i++)
    {
        throwErrorWithMemLeak();
    }
 
    return 0;
}
