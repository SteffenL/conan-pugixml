from conans import ConanFile, CMake
from conans import tools
import os
import sys

class PugixmlConan(ConanFile):
    name = "pugixml"
    version = "1.7"
    url = "https://github.com/SteffenL/conan-pugixml"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports = "CMakeLists.txt"

    git_repository_url = "https://github.com/zeux/pugixml"

    def source(self):
        git_branch = "v" + self.version

        if not os.path.exists("pugixml"):
            os.mkdir("pugixml")
        os.chdir("pugixml")

        if sys.version_info.major >= 3:
            self.run("git clone --depth 1 --branch {0} {1} .".format(git_branch, self.git_repository_url))
        else:
            # Workaround for Python versions earlier than 3.0:
            # Instead of cloning the whole repository, we pull only what we need.
            # The reason is that pugixml includes test-files with unicode characters in the path, which causes problems in earlier versions of Python.

            self.run("git init")
            self.run("git remote add origin %s" % self.git_repository_url)
            self.run("git config core.sparsecheckout true")
            self.run("echo src>>.git/info/sparse-checkout")
            self.run("git pull origin %s" % git_branch)

    def build(self):
        if self.options.shared and self.settings.compiler == "Visual Studio":
            tools.replace_in_file("pugixml/src/pugiconfig.hpp", "#endif", """
#ifdef _DLL
    #define PUGIXML_API __declspec(dllexport)
#else
    #define PUGIXML_API __declspec(dllimport)
#endif

#endif
""")

        cmake = CMake(self.settings)
        flags = " ".join([
            "-DBUILD_SHARED_LIBS={0}".format("ON" if self.options.shared else "OFF")
        ])
        self.run("cmake . %s %s" % (cmake.command_line, flags))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy(pattern="*.hpp", dst="include", src="pugixml/src")
        self.copy(pattern="*.lib", dst="lib", src="lib")
        self.copy(pattern="*.a", dst="lib", src="lib")
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.so*", dst="lib", src="lib")
        self.copy(pattern="*.dylib*", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["pugixml"]
