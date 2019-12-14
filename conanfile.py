from conans import ConanFile, CMake, tools


class VoltnetConan(ConanFile):
    name = "volt_net"
    version = "0.0.1"
    license = "GPL3"
    author = "Ovidiu Opris opris.ovidiu@gmail.com"
    url = "https://www.github.com/SirHall/volt_net_conan"
    requires = "volt_event/0.0.1@volt/dev"
    description = "Library that handles network connections"
    topics = ("C++", "Networking", "Crossplatform")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"

    def source(self):
        git = tools.Git(folder="volt_net")
        git.clone("https://www.github.com/SirHall/volt_net.git", "master")

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("volt_net/CMakeLists.txt", "project(volt_ge_net)",
                              '''project(volt_ge_net)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="volt_net")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    # def package_info(self):
    #     self.cpp_info.libs = ["hello"]
