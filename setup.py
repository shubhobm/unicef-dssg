# setup.py
import os

from packaging_tools.setup_utils import BuildHelper
from setuptools import Extension, dist, find_packages, setup
from setuptools.command.egg_info import egg_info

PACKAGE_NAME = "unicef-dssg"

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./"))

build_helper = BuildHelper()
build_helper.configure_package_root_path(root_path)

setup(
    name=PACKAGE_NAME,
    cmdclass={},
    version=build_helper.get_build_version(PACKAGE_NAME, "0.0.1", "dev"),
    include_package_data=False,  # this line is required to make "package_data" work correctly
    package_data={
        PACKAGE_NAME: [*build_helper.get_all_files(PACKAGE_NAME)],
        "scripts": [*build_helper.get_all_files("scripts")],
        "packaging_tools": [*build_helper.get_all_files("packaging_tools")],
    },
    install_requires=[],
)
