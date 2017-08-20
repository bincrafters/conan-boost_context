from conans import ConanFile, tools, os

class BoostContextConan(ConanFile):
    name = "Boost.Context"
    version = "1.64.0"
    generators = "boost" 
    settings = "os", "arch", "compiler", "build_type"
    short_paths = True
    url = "https://github.com/bincrafters/conan-boost-context"
    source_url = "https://github.com/boostorg/context"
    description = "Please visit http://www.boost.org/doc/libs/1_64_0/libs/libraries.htm"
    license = "www.boost.org/users/license.html"
    lib_short_names = ["context"]
    build_requires = "Boost.Generator/0.0.1@bincrafters/testing"
    requires =  "Boost.Assert/1.64.0@bincrafters/testing", \
                      "Boost.Config/1.64.0@bincrafters/testing", \
                      "Boost.Pool/1.64.0@bincrafters/testing", \
                      "Boost.Predef/1.64.0@bincrafters/testing", \
                      "Boost.Smart_Ptr/1.64.0@bincrafters/testing", \
                      "Boost.Level11Group/1.64.0@bincrafters/testing"

                      #assert1 config0 pool11 predef0 smart_ptr4
                      
    def source(self):
        for lib_short_name in self.lib_short_names:
            self.run("git clone --depth=1 --branch=boost-{0} https://github.com/boostorg/{1}.git"
                     .format(self.version, lib_short_name)) 

    def build(self):
        self.run(self.deps_user_info['Boost.Generator'].b2_command)
        
        with open(os.path.join(self.build_folder,"stage","lib","jamroot.jam"),"a") as f:
            f.write("""
import feature ;
feature.feature segmented-stacks : on : optional propagated composite ;
feature.compose <segmented-stacks>on : <define>BOOST_USE_SEGMENTED_STACKS ;
""")
        
    def package(self):
        for lib_short_name in self.lib_short_names:
            include_dir = os.path.join(lib_short_name, "include")
            self.copy(pattern="*", dst="include", src=include_dir)		

        self.copy(pattern="*", dst="lib", src="stage/lib")

    def package_info(self):
        self.user_info.lib_short_names = (",").join(self.lib_short_names)
        self.cpp_info.libs = self.collect_libs()
