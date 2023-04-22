from entity import Entity, attribute

from typing import Dict
import subprocess

class GitRepo(Entity):
    """
    Represents a Git repository.
    """
    def __init__(self, url: str, rev: str, repo_info: Dict, files: Dict[str, str]):
        """Creates a new Git repository instance"""
        super().__init__(id)
        self._url = url
        self._rev = rev
        self._repo_info = repo_info
        self._files = files

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

    @property
    @attribute
    def files(self):
        return self._files

    def pyproject_toml(self):
        return self._files.get("pyproject.toml", None)

    def pipfile(self):
        return self._files.get("Pipfile", None)

    def poetry_lock(self):
        return self._files.get("poetry.lock", None)

    @classmethod
    def url_is_a_git_repo(cls, url: str) -> bool:
        try:
            subprocess.check_output(['git', 'ls-remote', url], stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False