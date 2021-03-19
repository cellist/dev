#include <boost/scoped_array.hpp>
 
void throwErrorWithMemLeak()
{
    try
    {
        // Allocate 1kB buffer in an scoped pointer
        boost::scoped_array<char> buffer( new char[1024] );
 
        // Throw
        throw 1;
 
    }
    catch(const int e)
    {
    }
}
 
int main(int args, char **argc)
{
    // A simple case of when an exception doesn't lead to a memory leak
 
    // Iterate the throwing function 1024 times, creating a possible 1MB
    // memory leak, but scoped_array prevents it gracefully.
    for (size_t i=0; i<1024; i++)
    {
        throwErrorWithMemLeak();
    }
 
    return 0;
}
