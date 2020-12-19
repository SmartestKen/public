cmake_minimum_required(VERSION 3.15)
project(transproxy)

include_directories(/usr/include)
link_directories(/usr/local/lib)


# set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "-fpermissive")
add_executable(transproxy main.cpp)

# project name, event -> libevent.a
target_link_libraries(transproxy event)
