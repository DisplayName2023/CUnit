cmake_minimum_required(VERSION 3.10)
project(CUnit)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


set( INTERPROCEDURAL_OPTIMIZATION OFF )
# set( CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON )

# Options
option(BUILD_SHARED_LIBS "Build shared libraries" ON)
option(BUILD_TESTING "Build test applications" ON)

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Add source files
set(CUNIT_SOURCES
    CUnit/Sources/Framework/CUError.c
    CUnit/Sources/Framework/MyMem.c
    CUnit/Sources/Framework/TestDB.c
    CUnit/Sources/Framework/TestRun.c
    CUnit/Sources/Framework/Util.c
    CUnit/Sources/Console/Console.c
    CUnit/Sources/Basic/Basic.c
    CUnit/Sources/Automated/Automated.c
)

# Add header files
set(CUNIT_HEADERS
    CUnit/Headers/CUError.h
    CUnit/Headers/MyMem.h
    CUnit/Headers/TestDB.h
    CUnit/Headers/TestRun.h
    CUnit/Headers/Util.h
    CUnit/Headers/Console.h
    CUnit/Headers/Basic.h
    CUnit/Headers/Automated.h
    CUnit/Headers/CUnit.h
    CUnit/Headers/CUnit_intl.h
)

# Create library
add_library(cunit ${CUNIT_SOURCES} ${CUNIT_HEADERS})




# Set library properties
set_target_properties(cunit PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
    PUBLIC_HEADER "${CUNIT_HEADERS}"
    C_VISIBILITY_PRESET hidden
)

# Add DLL export definitions
if(WIN32 AND BUILD_SHARED_LIBS)
    target_compile_definitions(cunit PRIVATE 
        CUNIT_DLL_EXPORTS
        CU_DLL=1
        CU_BUILD_DLL
    )
else()
endif()

# Include directories
target_include_directories(cunit
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/CUnit/Headers
)

# Installation
install(TARGETS cunit
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    PUBLIC_HEADER DESTINATION include
)

# Test applications
if(BUILD_TESTING)
    # Example Tests source
    set(EXAMPLE_TESTS_SOURCES
        Examples/ExampleTests.c
    )
    set(EXAMPLE_TESTS_HEADERS
        Examples/ExampleTests.h
    )

    # Test CUnit executable
    add_executable(test_cunit
        CUnit/Sources/Test/test_cunit.c
        CUnit/Sources/Framework/Util.c
        CUnit/Sources/Framework/CUError.c
        CUnit/Sources/Framework/TestDB.c
        CUnit/Sources/Framework/TestRun.c
        CUnit/Sources/Framework/MyMem.c
    )
    target_link_libraries(test_cunit cunit)
    target_include_directories(test_cunit PRIVATE 
        ${CMAKE_CURRENT_SOURCE_DIR}/CUnit/Headers
        ${CMAKE_CURRENT_SOURCE_DIR}/Examples
    )
    target_compile_definitions(test_cunit PRIVATE CUNIT_BUILD_TESTS MEMTRACE _CRT_SECURE_NO_WARNINGS)

    target_include_directories( test_cunit
        PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/CUnit/Sources/Test
    )
   

    


    # Basic Test
    add_executable(basic_test
        Examples/BasicTest/BasicTest.c
        ${EXAMPLE_TESTS_SOURCES}
    )
    target_link_libraries(basic_test PRIVATE cunit)
    target_include_directories(basic_test PRIVATE 
        ${CMAKE_CURRENT_SOURCE_DIR}/CUnit/Headers
        ${CMAKE_CURRENT_SOURCE_DIR}/Examples
    )
    target_compile_definitions(basic_test PRIVATE _CRT_SECURE_NO_WARNINGS)

    # Console Test
    add_executable(console_test
        Examples/ConsoleTest/ConsoleTest.c
        ${EXAMPLE_TESTS_SOURCES}
    )
    target_link_libraries(console_test PRIVATE cunit)
    target_include_directories(console_test PRIVATE 
        ${CMAKE_CURRENT_SOURCE_DIR}/CUnit/Headers
        ${CMAKE_CURRENT_SOURCE_DIR}/Examples
    )
    target_compile_definitions(console_test PRIVATE _CRT_SECURE_NO_WARNINGS)

    # Automated Test
    add_executable(automated_test
        Examples/AutomatedTest/AutomatedTest.c
        ${EXAMPLE_TESTS_SOURCES}
    )
    target_link_libraries(automated_test PRIVATE cunit)
    target_include_directories(automated_test PRIVATE 
        ${CMAKE_CURRENT_SOURCE_DIR}/CUnit/Headers
        ${CMAKE_CURRENT_SOURCE_DIR}/Examples
    )
    target_compile_definitions(automated_test PRIVATE _CRT_SECURE_NO_WARNINGS)
endif() 