import os
import re

import pkg_resources


class BuildHelper:
    def __init__(self):
        self.package_root_path = "/nonexistentpath"

    def configure_package_root_path(self, new_root_path):
        self.package_root_path = new_root_path

    def extract_version_from_pkg_info(self, pkg_info_content):
        name_pattern = re.compile("^Version: (.*)", flags=re.MULTILINE)
        version = name_pattern.search(pkg_info_content).group(1)
        return version

    def get_stored_package_version(self, package_name):

        is_pkg_info_present = os.path.isfile(os.path.join(self.package_root_path, "PKG-INFO"))
        version = None

        if is_pkg_info_present:
            pkg_info_stream = os.popen(f"cd {self.package_root_path} && cat PKG-INFO")
            pkg_info_output = pkg_info_stream.read().strip()

            version = self.extract_version_from_pkg_info(pkg_info_output)

        return version

    def get_build_version(self, package_name, current_version, build_prefix):
        stored_package_version = self.get_stored_package_version(package_name)
        generated_build_version = None
        potential_build_version = "not-a-valid-version"
        is_git_directory_present = os.path.isdir(os.path.join(self.package_root_path, ".git"))

        if stored_package_version:
            potential_build_version = stored_package_version
        elif is_git_directory_present:
            build_number_stream = os.popen(
                f"cd {self.package_root_path} && git rev-list --count HEAD"
            )
            build_number_output = build_number_stream.read().strip()

            print(f"Generated build number output: ###{build_number_output}###")
            potential_build_version = f"{current_version}.{build_prefix}{build_number_output}"
        else:
            raise RuntimeError("Can't generate package build version")

        generated_build_version = pkg_resources.parse_version(potential_build_version)

        if (
            not generated_build_version
            or type(generated_build_version) is not pkg_resources.extern.packaging.version.Version
        ):
            raise RuntimeError(f"Incorrect version format: {generated_build_version}")

        return f"{generated_build_version}"

    def get_all_files(self, relative_content_path):
        content_absolute_path = os.path.join(
            f"{self.package_root_path}", f"{relative_content_path}"
        )
        vendored_dir_tree = os.walk(content_absolute_path)
        vendored_file_paths = []

        for current_dir, dirs, located_files in vendored_dir_tree:
            if len(located_files) == 0:
                continue

            for file_name in located_files:
                relative_path = os.path.join(current_dir, f"{file_name}".strip())
                # print(glob.escape(relative_path))
                vendored_file_paths.append(relative_path)

        return vendored_file_paths
