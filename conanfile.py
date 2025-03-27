from conan import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get, copy, rmdir
from conan.tools.layout import cmake_layout
import os

class CUnitConan(ConanFile):
    name = "conan_cunit"
    version = "2.1-3"
    description = "A Unit Testing Framework for C"
    license = "LGPL-2.1-or-later"
    url = "https://github.com/jacklicn/CUnit"
    homepage = "https://github.com/jacklicn/CUnit"
    topics = ("unit-test", "testing", "c")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_testing": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "build_testing": False,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def export_sources(self):
        # Export all source files and CMake files
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)
        copy(self, "CUnit/*", self.recipe_folder, self.export_sources_folder)
        copy(self, "Examples/*", self.recipe_folder, self.export_sources_folder)
        copy(self, "COPYING", self.recipe_folder, self.export_sources_folder)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["BUILD_TESTING"] = self.options.build_testing
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        
        # Copy license file
        copy(self, "COPYING", src=self.export_sources_folder, dst=os.path.join(self.package_folder, "licenses"))
        
        # Remove unnecessary files
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "CUnit")
        self.cpp_info.set_property("cmake_target_name", "CUnit::cunit")
        self.cpp_info.set_property("pkg_config_name", "cunit")

        # Libraries
        self.cpp_info.libs = ["cunit"]
        if self.settings.os == "Windows" and self.options.shared:
            self.cpp_info.defines = ["CUNIT_DLL"]

        # Include directories
        self.cpp_info.includedirs = ["include"]

        # Build type specific settings
        if self.settings.build_type == "Debug":
            self.cpp_info.defines.append("CU_DLL=1")
            if self.options.shared:
                self.cpp_info.defines.append("CU_BUILD_DLL")

        # Set package info
        self.cpp_info.names["cmake_find_package"] = "CUnit"
        self.cpp_info.names["cmake_find_package_multi"] = "CUnit" 