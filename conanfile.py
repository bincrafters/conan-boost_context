from conans import ConanFile, tools, os

class BoostContextConan(ConanFile):
    name = "Boost.Context"
    version = "1.64.0"
    generators = "boost" 
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/boostorg/context"
    description = "Please visit http://www.boost.org/doc/libs/1_64_0/libs/libraries.htm"
    license = "www.boost.org/users/license.html"
    lib_short_name = "context"
    build_requires = "Boost.Generator/0.0.1@bincrafters/testing"
    requires =  "Boost.Assert/1.64.0@bincrafters/testing", \
                      "Boost.Config/1.64.0@bincrafters/testing", \
                      "Boost.Pool/1.64.0@bincrafters/testing", \
                      "Boost.Predef/1.64.0@bincrafters/testing", \
                      "Boost.Smart_Ptr/1.64.0@bincrafters/testing"

                      #assert1 config0 pool11 predef0 smart_ptr4
                      
    def source(self):
        self.run("git clone --depth=50 --branch=boost-{0} {1}.git"
                 .format(self.version, self.url))

    def build(self):
        boost_build = self.deps_cpp_info["Boost.Build"]
        b2_bin_name = "b2.exe" if self.settings.os == "Windows" else "b2"
        b2_bin_dir_name = boost_build.bindirs[0]
        b2_full_path = os.path.join(boost_build.rootpath, b2_bin_dir_name, b2_bin_name)

        toolsets = {
          'gcc': 'gcc',
          'Visual Studio': 'msvc',
          'clang': 'clang',
          'apple-clang': 'darwin'}

        b2_toolset = toolsets[str(self.settings.compiler)]
        
        self.run(b2_full_path + " -j4 -a --hash=yes toolset=" + b2_toolset)
        
    def package(self):
        include_dir = os.path.join(self.build_folder, self.lib_short_name, "include")
        self.copy(pattern="*", dst="include", src=include_dir)
        lib_dir = os.path.join(self.build_folder, "stage/lib")
        self.copy(pattern="*", dst="lib", src=lib_dir)

    def package_info(self):
        self.cpp_info.libs = ["boost_%s"%(self.lib_short_name)]
