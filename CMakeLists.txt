cmake_minimum_required(VERSION 2.8)
project(LOG6302)

set(CMAKE_C_COMPILER /usr/bin/clang)
set(CMAKE_CXX_COMPILER /usr/bin/clang++)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-rtti")
set(SOURCE_FILES src/main.cpp src/Visitor.cpp src/Visitor.h)

# LOG6302
# CHANGER LA VALEUR DE "LLVM_PATH" EN DESSOUS POUR UTILISER UNE AUTRE VERSION DE CLANG
# NORMALEMENT, LLVM_PATH DOIT CONTENIR LES DOSSIERS "lib" ET "include".
set(LLVM_PATH /usr/lib/llvm-16)

set(USE_OLD_CLANG true)
# if (EXISTS "${LLVM_PATH}/lib/libLLVMProfileData.so")
#     set(USE_OLD_CLANG false)
#     MESSAGE(STATUS "Using recent version of LLVM/Clang")
# else()
#     MESSAGE(STATUS "Using old version of LLVM/Clang")
# endif()

include_directories(
        ${LLVM_PATH}/include
        /usr/include
        /usr/include/c++
)
link_directories(${LLVM_PATH}/lib)
add_definitions(-DLLVM_PATH=\"${LLVM_PATH}\")

add_definitions(-D__STDC_LIMIT_MACROS -D__STDC_CONSTANT_MACROS )
if (NOT USE_OLD_CLANG)
    add_definitions(-D_GLIBCXX_USE_CXX11_ABI=1)
else()
    add_definitions(-D_GLIBCXX_USE_CXX11_ABI=0)
endif()

add_executable(${PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(
        ${PROJECT_NAME}

        clangFrontend
        clangFrontendTool
        clangParse
        clangSema
        clangAST
        clangSerialization
        clangAnalysis
        clangDriver
        clangASTMatchers
        clangEdit
        clangLex
        clangBasic
        clangTooling

        LLVMMC
        LLVMMCParser
        LLVMBitReader
        LLVMCore
        LLVMSupport
        LLVMOption

        tinfo
        pthread
        dl
        z
)
if (NOT USE_OLD_CLANG)
    target_link_libraries(
            ${PROJECT_NAME}
            LLVMProfileData
    )
endif()
