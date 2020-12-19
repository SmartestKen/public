cmake_minimum_required(VERSION 3.15)
project(transproxy_c C)

set(CMAKE_C_STANDARD 11)

include_directories(/usr/local/include/)
link_directories(/usr/local/lib)

add_executable(transproxy_c
        main.h main.c)

target_link_libraries(transproxy_c crypto)
target_link_libraries(transproxy_c ssl)
target_link_libraries(transproxy_c event)
