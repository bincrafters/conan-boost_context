from conans import ConanFile, tools, os


class BoostContextConan(ConanFile):
    name = "Boost.Context"
    version = "1.65.1"
    generators = "boost" 
    settings = "os", "arch", "compiler", "build_type"
    short_paths = True
    url = "https://github.com/bincrafters/conan-boost-context"
    description = "Please visit http://www.boost.org/doc/libs/1_65_1/libs/libraries.htm"
    license = "www.boost.org/users/license.html"
    lib_short_names = ["context"]
    options = {"shared": [True, False]}
    default_options = "shared=False"
    build_requires = "Boost.Generator/1.65.1@bincrafters/testing"
    requires =  "Boost.Assert/1.65.1@bincrafters/testing", \
                      "Boost.Config/1.65.1@bincrafters/testing", \
                      "Boost.Pool/1.65.1@bincrafters/testing", \
                      "Boost.Predef/1.65.1@bincrafters/testing", \
                      "Boost.Smart_Ptr/1.65.1@bincrafters/testing", \
                      "Boost.Level11Group/1.65.1@bincrafters/testing"

                      #assert1 config0 pool11 predef0 smart_ptr4
                      
    def source(self):
        boostorg_github = "https://github.com/boostorg"
        archive_name = "boost-" + self.version  
        for lib_short_name in self.lib_short_names:
            tools.get("{0}/{1}/archive/{2}.tar.gz"
                .format(boostorg_github, lib_short_name, archive_name))
            os.rename(lib_short_name + "-" + archive_name, lib_short_name)

    def build(self):
        self.run(self.deps_user_info['Boost.Generator'].b2_command + " " + self.b2_args)
        
        with open(os.path.join(self.build_folder,"stage","lib","jamroot.jam"),"a") as f:
            f.write("""
import feature ;
feature.feature segmented-stacks : on : optional propagated composite ;
feature.compose <segmented-stacks>on : <define>BOOST_USE_SEGMENTED_STACKS ;
""")
        
    def package(self):
        self.copy(pattern="*", dst="lib", src="stage/lib")
        for lib_short_name in self.lib_short_names:
            include_dir = os.path.join(lib_short_name, "include")
            self.copy(pattern="*", dst="include", src=include_dir)

    def package_info(self):
        self.user_info.lib_short_names = ",".join(self.lib_short_names)
        self.cpp_info.libs = self.collect_libs()
        self.cpp_info.defines.append("BOOST_ALL_NO_LIB=1")

    @property
    def b2_args(self):
        binary_format_arg = "binary-format="+self.b2_binary_format if self.b2_binary_format else ""
        abi_arg = "abi="+self.b2_abi if self.b2_abi else ""
        return binary_format_arg+" "+abi_arg

    @property
    def b2_binary_format(self):
        if self.settings.os == "iOS" or self.settings.os == "Macos":
            return "mach-o"
        elif self.settings.os == "Android" or self.settings.os == "Linux":
            return "elf"
        elif self.settings.os == "Windows":
            return  "pe"
        else:
            return None

    @property
    def b2_abi(self):
        if str(self.settings.arch).startswith('x86'):
            if self.settings.os == "Windows":
                return "ms"
            else:
                return "sysv"
        elif str(self.settings.arch).startswith('ppc'):
            return "sysv"
        elif str(self.settings.arch).startswith('arm'):
            return "aapcs"
        else:
            return None
