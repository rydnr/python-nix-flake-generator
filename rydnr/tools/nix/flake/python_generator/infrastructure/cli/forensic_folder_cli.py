# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/infrastructure/cli/forensic_folder_cli.py

This file defines the ForensicFolderCli class.

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
from domain.primary_port import PrimaryPort

import argparse


class ForensicFolderCli(PrimaryPort):

    """
    A PrimaryPort that configures the forensic folder from the command line.
    """

    def __init__(self):
        super().__init__()

    def priority(self) -> int:
        return 1

    async def accept(self, app):
        parser = argparse.ArgumentParser(description="Parses the forensic folder")
        parser.add_argument(
            "-x",
            "--forensic_folder",
            required=True,
            help="The folder where to copy the contents of flakes whose build failed",
        )
        args, unknown_args = parser.parse_known_args()
        await app.accept_forensic_folder(args.forensic_folder)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End: