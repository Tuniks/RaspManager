TEMPLATE = lib
TARGET = Botan

PRECOMPILED_HEADER = ../precompiled_headers/botan_pch.h

CONFIG += exceptions

include(../../../qtcreatorlibrary.pri)

DEPENDPATH += .
INCLUDEPATH += .

DEFINES += BOTAN_DLL=Q_DECL_EXPORT
unix:DEFINES += BOTAN_TARGET_OS_HAS_GETTIMEOFDAY BOTAN_HAS_ALLOC_MMAP \
    BOTAN_HAS_ENTROPY_SRC_DEV_RANDOM BOTAN_HAS_ENTROPY_SRC_EGD BOTAN_HAS_ENTROPY_SRC_FTW \
    BOTAN_HAS_ENTROPY_SRC_UNIX BOTAN_HAS_MUTEX_PTHREAD BOTAN_HAS_PIPE_UNIXFD_IO
*linux*:DEFINES += BOTAN_TARGET_OS_IS_LINUX BOTAN_TARGET_OS_HAS_CLOCK_GETTIME \
    BOTAN_TARGET_OS_HAS_DLOPEN BOTAN_TARGET_OS_HAS_GMTIME_R BOTAN_TARGET_OS_HAS_POSIX_MLOCK \
    BOTAN_HAS_DYNAMICALLY_LOADED_ENGINE BOTAN_HAS_DYNAMIC_LOADER
macx:DEFINES += BOTAN_TARGET_OS_IS_DARWIN
*g++*:DEFINES += BOTAN_BUILD_COMPILER_IS_GCC
*clang*:DEFINES += BOTAN_BUILD_COMPILER_IS_CLANG
*icc*:DEFINES += BOTAN_BUILD_COMPILER_IS_INTEL

win32 {
    DEFINES += BOTAN_TARGET_OS_IS_WINDOWS \
        BOTAN_TARGET_OS_HAS_LOADLIBRARY BOTAN_TARGET_OS_HAS_WIN32_GET_SYSTEMTIME \
        BOTAN_TARGET_OS_HAS_WIN32_VIRTUAL_LOCK BOTAN_HAS_DYNAMICALLY_LOADED_ENGINE \
        BOTAN_HAS_DYNAMIC_LOADER BOTAN_HAS_ENTROPY_SRC_CAPI BOTAN_HAS_ENTROPY_SRC_WIN32 \
        BOTAN_HAS_MUTEX_WIN32

    win32-msvc* {
        QMAKE_CXXFLAGS += -wd4251 -wd4290 -wd4250
        DEFINES += BOTAN_BUILD_COMPILER_IS_MSVC BOTAN_TARGET_OS_HAS_GMTIME_S
    } else {
        QMAKE_CFLAGS += -fpermissive -finline-functions -Wno-long-long
        QMAKE_CXXFLAGS += -fpermissive -finline-functions -Wno-long-long
    }
    LIBS += -ladvapi32 -luser32
}

unix:*-g++* {
    QMAKE_CFLAGS += -fPIC -ansi -fpermissive -finline-functions -Wno-long-long
    QMAKE_CXXFLAGS += -fPIC -ansi -fpermissive -finline-functions -Wno-long-long
    QMAKE_CXXFLAGS_HIDESYMS -= -fvisibility-inlines-hidden # for ubuntu 7.04
}

HEADERS += botan.h
SOURCES += botan.cpp

linux*|freebsd* {
    LIBS += -lrt
}