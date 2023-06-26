#include <iostream>
#include <thread>

// Function to be executed in the separate thread
void threadFunction() {
    std::cout << "This is a separate thread." << std::endl;
}

int main() {
    // Create a thread and execute the threadFunction
    std::thread t(threadFunction);

    // Wait for the thread to finish execution
    t.join();

    // Main thread continues here
    std::cout << "Back in the main thread." << std::endl;

    return 0;
}
