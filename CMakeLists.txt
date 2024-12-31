cmake_minimum_required(VERSION 3.10)
project(QproCppTemplate)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 添加源文件目录
include_directories(${PROJECT_SOURCE_DIR}/include)

# 添加可执行文件
add_executable(${PROJECT_NAME} 
    main.cpp
)
