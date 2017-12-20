from conans import ConanFile


class BoostContextConan(ConanFile):
    name = "Boost.Context"
    version = "1.65.1"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    requires = \
        "Boost.Assert/1.65.1@bincrafters/testing", \
        "Boost.Config/1.65.1@bincrafters/testing", \
        "Boost.Pool/1.65.1@bincrafters/testing", \
        "Boost.Predef/1.65.1@bincrafters/testing", \
        "Boost.Smart_Ptr/1.65.1@bincrafters/testing", \
        "Boost.Thread/1.65.1@bincrafters/testing"
    lib_short_names = ["context"]
    is_header_only = False

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

    url = "https://github.com/bincrafters/conan-boost-context"
    description = "Please visit http://www.boost.org/doc/libs/1_65_1"
    license = "www.boost.org/users/license.html"
    build_requires = "Boost.Generator/1.65.1@bincrafters/testing"
    short_paths = True
    generators = "boost"
    settings = "os", "arch", "compiler", "build_type"
    exports = "boostgenerator.py"

    def package_id(self):
        getattr(self, "package_id_after", lambda:None)()
    def source(self):
        self.call_patch("source")
    def build(self):
        self.call_patch("build")
    def package(self):
        self.call_patch("package")
    def package_info(self):
        self.call_patch("package_info")
    def call_patch(self, method, *args):
        if not hasattr(self, '__boost_conan_file__'):
            try:
                from conans import tools
                with tools.pythonpath(self):
                    import boostgenerator  # pylint: disable=F0401
                    boostgenerator.BoostConanFile(self)
            except Exception as e:
                self.output.error("Failed to import boostgenerator for: "+str(self)+" @ "+method.upper())
                raise e
        return getattr(self, method, lambda:None)(*args)
    @property
    def env(self):
        import os.path
        result = super(self.__class__, self).env
        result['PYTHONPATH'] = [os.path.dirname(__file__)] + result.get('PYTHONPATH',[])
        return result
    @property
    def build_policy_missing(self):
        return (getattr(self, 'is_in_cycle_group', False) and not getattr(self, 'is_header_only', True)) or super(self.__class__, self).build_policy_missing

    # END
