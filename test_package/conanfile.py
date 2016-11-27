from conans import ConanFile, CMake
import os

class RunConanTestConan(ConanFile):
    _conan_user = os.getenv("CONAN_USERNAME", "sl")
    _conan_channel = os.getenv("CONAN_CHANNEL", "testing")

    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    requires = "pugixml/1.7@{0}/{1}".format(_conan_user, _conan_channel)

    def build(self):
        cmake = CMake(self.settings)
        self.run("cmake \"%s\" %s" % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib*", dst="bin", src="lib")

    def test(self):
        os.chdir("bin")
        self.run(os.path.join(".", "run_conan_test"))
