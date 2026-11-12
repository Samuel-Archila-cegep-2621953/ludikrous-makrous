cmake_minimum_required(VERSION 3.23)

add_subdirectory(cryptopp)

project(DRM)

add_executable(DRM main.cpp)

target_link_libraries(DRM PRIVATE cryptopp)