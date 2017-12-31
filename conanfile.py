#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools


class BoostContextConan(ConanFile):
    name = "boost_context"
    version = "1.66.0"
    url = "https://github.com/bincrafters/conan-boost_context"
    
    lib_short_names = ["context"]
    is_header_only = False
    
    options = {"shared": [True, False]}
    default_options = "shared=False"
    
    requires = (
        "boost_package_tools/1.66.0@bincrafters/testing",
        "boost_assert/1.66.0@bincrafters/testing",
        "boost_config/1.66.0@bincrafters/testing",
        "boost_pool/1.66.0@bincrafters/testing",
        "boost_predef/1.66.0@bincrafters/testing",
        "boost_smart_ptr/1.66.0@bincrafters/testing",
        "boost_thread/1.66.0@bincrafters/testing"
    )

    def build_after(self):
        import os
        with open(os.path.join(self.build_folder, "context", "lib", "jamroot.jam"), "a") as f:
            f.write("""
import feature ;
feature.feature segmented-stacks : on : optional propagated composite ;
feature.compose <segmented-stacks>on : <define>BOOST_USE_SEGMENTED_STACKS ;
""")

    def b2_options(self, lib_name=None):
        # pylint: disable=unused-argument
        return " " + self.b2_args

    @property
    def b2_args(self):
        binary_format_arg = "binary-format=" + self.b2_binary_format if self.b2_binary_format else ""
        abi_arg = "abi=" + self.b2_abi if self.b2_abi else ""
        return binary_format_arg + " " + abi_arg

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

    # BEGIN

    description = "Please visit http://www.boost.org/doc/libs/1_66_0"
    license = "BSL-1.0"
    build_requires = "boost_generator/1.66.0@bincrafters/testing"
    short_paths = True
    generators = "boost"
    settings = "os", "arch", "compiler", "build_type"

    def package_id(self):
        getattr(self, "package_id_additional", lambda:None)()

    def source(self):
        with tools.pythonpath(self):
            import boost_package_tools  # pylint: disable=F0401
            boost_package_tools.source(self)
        getattr(self, "source_additional", lambda:None)()

    def build(self):
        with tools.pythonpath(self):
            import boost_package_tools  # pylint: disable=F0401
            boost_package_tools.build(self)
        getattr(self, "build_additional", lambda:None)()

    def package(self):
        with tools.pythonpath(self):
            import boost_package_tools  # pylint: disable=F0401
            boost_package_tools.package(self)
        getattr(self, "package_additional", lambda:None)()

    def package_info(self):
        with tools.pythonpath(self):
            import boost_package_tools  # pylint: disable=F0401
            boost_package_tools.package_info(self)
        getattr(self, "package_info_additional", lambda:None)()



    # END
