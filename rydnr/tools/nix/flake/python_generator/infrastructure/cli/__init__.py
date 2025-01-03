# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/infrastructure/cli/__init__.py

This file ensures rydnr.tools.nix.flake.python_generator.infrastructure.cli is a namespace.

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

from .package_name_cli import PackageNameCli
from .package_version_cli import PackageVersionCli
from .build_flake_cli import BuildFlakeCli
from .create_flake_cli import CreateFlakeCli
from .flakes_folder_cli import FlakesFolderCli
from .flakes_url_cli import FlakesUrlCli
from .forensic_folder_cli import ForensicFolderCli
from .github_token_cli import GithubTokenCli
from .recipes_folder_cli import RecipesFolderCli

# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
