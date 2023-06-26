cmake_minimum_required(VERSION 3.12)
project(TCPClientServerExample)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Find the Threads package
find_package(Threads REQUIRED)

# Add the server executable target
add_executable(server server.cpp)
target_link_libraries(server PRIVATE Threads::Threads)

# Add the client executable target
add_executable(client client.cpp)
target_link_libraries(client PRIVATE Threads::Threads)
