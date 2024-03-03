# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/python_package_metadata.py

This file defines the PythonPackageMetadata entity.

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
from pythoneda.shared import attribute, Entity, primary_key_attribute

from typing import Dict


class PythonPackageMetadata(Entity):
    """
    Represents metadata of a Python package.
    """

    def __init__(self, name: str, version: str, info: Dict, release: Dict):
        """Creates a new PythonPackageMetadata instance"""
        super().__init__()
        self._name = name
        self._version = version
        self._info = info
        self._release = release

    @property
    @primary_key_attribute
    def name(self) -> str:
        return self._name

    @property
    @primary_key_attribute
    def version(self) -> str:
        return self._version

    @property
    @attribute
    def info(self) -> Dict:
        return self._info

    @property
    @attribute
    def release(self) -> Dict:
        return self._release


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End: