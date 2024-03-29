# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/infrastructure/flake/folder_flake_repo.py

This file defines the FolderFlakeRepo class.

Copyright (C) 2023-today rydnr's rydnr/python-nix-flake-generator

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from rydnr.tools.nix.flake.python_generator.flake.flake import Flake
from rydnr.tools.nix.flake.python_generator.flake.flake_created import FlakeCreated
from rydnr.tools.nix.flake.python_generator.flake.flake_repo import FlakeRepo
from rydnr.tools.nix.flake.python_generator.flake.recipe.flake_recipe import FlakeRecipe

import logging
import os
from typing import Dict, List


class FolderFlakeRepo(FlakeRepo):
    """
    A FlakeRepo using a custom folder.
    """

    _repo_folder = None

    @classmethod
    def repo_folder(cls, folder: str):
        cls._repo_folder = folder

    _flakes_url = None

    @classmethod
    def flakes_url(cls, url: str):
        cls._flakes_url = url

    def flake_folder(self, package_name: str, package_version: str) -> str:
        return os.path.join(
            self.__class__._repo_folder, f"{package_name}-{package_version}"
        )

    def flake_nix_path(self, package_name: str, package_version: str) -> str:
        return os.path.join(
            self.flake_folder(package_name, package_version), "flake.nix"
        )

    def find_by_name_and_version(
        self, package_name: str, package_version: str
    ) -> Flake:
        """
        Retrieves the Flake matching given name and version, if any.
        """
        result = None

        if os.path.exists(self.flake_nix_path(package_name, package_version)):
            # TODO: parse the flake and retrieve the dependencies
            result = Flake(package_name, package_version, None, [], [], [], [], [])

        return result

    def create(
        self, flake: Flake, content: List[Dict[str, str]], recipe: FlakeRecipe
    ) -> FlakeCreated:
        #    def create(self, flake: Flake, flake_nix: str, flake_nix_path: str, package_nix: str, package_nix_path: str) -> FlakeCreated:
        """Creates the flake"""
        if self.find_by_name_and_version(flake.name, flake.version):
            logging.getLogger(__name__).warning(
                f"Not creating flake {flake.name}-{flake.version} since it already exists"
            )
            return None

        for item in content:
            if os.path.exists(os.path.join(self.__class__._repo_folder, item["path"])):
                logging.getLogger(__name__).debug(
                    f'Not overwriting {item["path"]} in {self.__class__._repo_folder}'
                )
            else:
                if not os.path.exists(
                    os.path.join(
                        self.__class__._repo_folder, os.path.dirname(item["path"])
                    )
                ):
                    os.makedirs(
                        os.path.join(
                            self.__class__._repo_folder, os.path.dirname(item["path"])
                        )
                    )

                with open(
                    os.path.join(self.__class__._repo_folder, item["path"]), "w"
                ) as file:
                    logging.getLogger(__name__).debug(f'Writing {item["path"]}')
                    file.write(item["contents"])

        return FlakeCreated(
            flake.name,
            flake.version,
            self.flake_folder(flake.name, flake.version),
            recipe,
        )

    def url_for_flake(self, name: str, version: str) -> str:
        """Retrieves the url of given flake"""
        return f"{self.__class__._flakes_url}{name}-{version}"


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
