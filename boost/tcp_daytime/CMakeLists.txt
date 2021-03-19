cmake_minimum_required(VERSION 3.13)

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

find_package(Boost 1.36.0 REQUIRED COMPONENTS
  system
)

if(Boost_FOUND)
  include_directories(${Boost_INCLUDE_DIRS})
  
  add_executable(client client.cpp)
  target_link_libraries(client
    ${Boost_LIBRARIES}
    Threads::Threads)

  add_executable(sync_server server.cpp)
  target_link_libraries(sync_server
    ${Boost_LIBRARIES}
    Threads::Threads)

  add_executable(async_server async_server.cpp)
  target_link_libraries(async_server
    ${Boost_LIBRARIES}
    Threads::Threads)
  
endif()
