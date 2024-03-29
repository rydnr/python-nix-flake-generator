# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/git/git_repo.py

This file defines the GitRepo class.

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
from pythoneda.shared import attribute, Entity
from rydnr.tools.nix.flake.python_generator.git import (
    ErrorCloningGitRepository,
    GitCheckoutFailed,
)

import logging
import os
import re
import subprocess
from urllib.parse import urlparse
from typing import Dict


class GitRepo(Entity):
    """
    Represents a Git repository.
    """

    def __init__(self, url: str, rev: str, repo_info: Dict, subfolder=None):
        """Creates a new Git repository instance"""
        super().__init__()
        self._url = url
        self._rev = rev
        self._repo_info = repo_info
        self._subfolder = subfolder
        self._files = {}

    @property
    @attribute
    def url(self):
        return self._url

    @property
    @attribute
    def rev(self):
        return self._rev

    @property
    @attribute
    def repo_info(self):
        return self._repo_info

    def is_monorepo(self):
        return self._subfolder is not None

    def get_file(self, fileName: str) -> str:
        """
        Retrieves the contents of given file in the repo.
        """
        result = self._files.get(fileName, None)
        if not result:
            result = self.access_file(fileName)
            self._files[fileName] = result

        return result

    @property
    @attribute
    def subfolder(self):
        return self._subfolder

    def access_file(self, fileName: str) -> str:
        """
        Retrieves the contents of given file in the repo
        """
        raise NotImplementedError("access_file() must be implemented by subclasses")

    def repo_owner_and_repo_name(self) -> tuple:
        return self.__class__.extract_repo_owner_and_repo_name(self.url)

    @classmethod
    def url_is_a_git_repo(cls, url: str) -> bool:
        try:
            subprocess.check_output(["git", "ls-remote", url], stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False

    @classmethod
    def extract_repo_owner_and_repo_name(cls, url: str) -> tuple:
        pattern = r"(?:https?://)?(?:www\.)?.*\.com/([^/]+)/([^/]+)"
        try:
            match = re.match(pattern, url)
            owner, repo_name = match.groups()
            return owner, repo_name

        except:
            logging.getLogger(cls.__name__).error(f"Invalid repo: {url}")

    def sha256(self):
        # Use nix-prefetch-git to compute the hash
        result = subprocess.run(
            ["nix-prefetch-git", "--deepClone", f"{self.url}/tree/{self.rev}"],
            check=True,
            capture_output=True,
            text=True,
        )
        output = result.stdout
        logging.getLogger(__name__).debug(
            f"nix-prefetch-git --deepClone {self.url}/tree/{self.rev} -> {output}"
        )

        return output.splitlines()[-1]

    def clone(self, folder: str, subfolder: str):
        result = os.path.join(folder, subfolder)

        try:
            subprocess.run(
                ["git", "clone", self.url, subfolder],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=folder,
            )
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise ErrorCloningGitRepository(self.url, folder)
        try:
            subprocess.run(
                ["git", "checkout", self.rev],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=result,
            )
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise GitCheckoutFailed(self.url, self.rev, folder)

        return result

    @classmethod
    def extract_url_and_subfolder(cls, url: str) -> tuple:
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split("/")

        if len(path_parts) > 4 and path_parts[3] == "tree":
            repo_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{path_parts[1]}/{path_parts[2]}"
            subfolder = "/".join(path_parts[5:])
        elif len(path_parts) > 3:
            repo_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{path_parts[1]}/{path_parts[2]}"
            subfolder = "/".join(path_parts[3:])
        else:
            repo_url = url
            subfolder = None

        return repo_url, subfolder

    def in_github(self) -> bool:
        parsed_url = urlparse(self.url)
        return parsed_url.netloc == "github.com"


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
