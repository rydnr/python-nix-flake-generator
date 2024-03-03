# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/nix/python/__init__.py

This file ensures rydnr.tools.nix.flake.python_generator.nix.python is a namespace.

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
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from .nix_python_package import NixPythonPackage
from .nix_python_package_in_nixpkgs import NixPythonPackageInNixpkgs
from .nix_python_package_repo import NixPythonPackageRepo

# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End: