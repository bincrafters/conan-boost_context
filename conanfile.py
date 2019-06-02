#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import python_requires, tools
import os


base = python_requires("boost_base/2.0.0@bincrafters/testing")


class BoostContextConan(base.BoostBaseConan):
    name = "boost_context"
    version = "1.70.0"

    def build(self):
        super(BoostContextConan, self).build()
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

    @property
    def boost_build_options(self):
        return {
            "binary-format": self.b2_binary_format,
            "abi": self.b2_abi,
        }

    @property
    def b2_binary_format(self):
        if self.settings.os == "iOS" or self.settings.os == "Macos":
            return "mach-o"
        elif self.settings.os == "Android" or self.settings.os == "Linux":
            return "elf"
        elif self.settings.os == "Windows":
            return "pe"
        else:
            return ""

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
            return ""
