#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import python_requires, tools
import os


base = python_requires("boost_base/1.68.0@bincrafters/stable")

class BoostContextConan(base.BoostBaseConan):
    name = "boost_context"
    url = "https://github.com/bincrafters/conan-boost_context"
    lib_short_names = ["context"]
    options = {"shared": [True, False]}
    default_options = "shared=False"
    b2_requires = [
        "boost_assert",
        "boost_config",
        "boost_pool",
        "boost_predef",
        "boost_smart_ptr",
        "boost_thread"
    ]

    def build_additional(self):
        jam_content = """
import feature ;
feature.feature segmented-stacks : on : optional propagated composite ;
feature.compose <segmented-stacks>on : <define>BOOST_USE_SEGMENTED_STACKS ;
"""
        tools.save(
            os.path.join(self.build_folder, "context", "lib", "jamroot.jam"),
            jam_content,
            append=True,
        )

    def get_b2_options(self):
        return self.b2_args

    @property
    def b2_args(self):
        return {
            "binary-format" : self.b2_binary_format if self.b2_binary_format else "",
            "abi" : self.b2_abi if self.b2_abi else "",
        }

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
