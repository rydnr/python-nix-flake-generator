from domain.ports import Ports
from domain.git_repo import GitRepo
from domain.python_package import PythonPackage

import toml
from typing import Dict, List

class PoetryPythonPackage(PythonPackage):
    """
    Represents a Poetry-based Python package.
    """
    def __init__(self, name: str, version: str, info: Dict, release: Dict, gitRepo: GitRepo):
        """Creates a new PoetryPythonPackage instance"""
        super().__init__(name, version, info, release, gitRepo)

    @classmethod
    def parse_toml(cls, contents: str) -> Dict:
        return toml.loads(contents)

    @classmethod
    def read_pyproject_toml(cls, gitRepo: GitRepo) -> Dict:
        result = {}
        if gitRepo:
            pyprojecttoml_contents = gitRepo.get_file("pyproject.toml")

            if pyprojecttoml_contents:
                result = cls.parse_toml(pyprojecttoml_contents)
        return result

    @classmethod
    def read_poetry_lock(cls, gitRepo) -> Dict:
        result = {}
        if gitRepo:
            poetrylock_contents = gitRepo.get_file("poetry.lock")

            if poetrylock_contents:
                result = cls.parse_toml(poetrylock_contents)
        return result

    @classmethod
    def git_repo_matches(cls, gitRepo: GitRepo) -> bool:
        result = False
        pyproject_toml = cls.read_pyproject_toml(gitRepo)

        if pyproject_toml:
            build_system_requires = pyproject_toml.get("build-system", {}).get("requires", [])
            if any(item.startswith("poetry") for item in build_system_requires):
                result = True
        return result

    def get_poetry_deps(self, section: str) -> List:
        result = []
        pyproject_toml = self.__class__.read_pyproject_toml()
        if pyproject_toml:
            poetry_lock = self.__class__.read_poetry_lock()
            if poetry_lock:
                for dev_dependency in list(pyproject_toml.get("tool", {}).get("poetry", {}).get(section, {}).keys()):
                    for package in poetry_lock["package"]:
                        if package.get("name", "") == dev_dependency:
                            pythonPackage = Ports.instance().resolvePythonPackageRepo().find_by_name_and_version(dev_dependency, package.get("version", ""))
                            if pythonPackage:
                                result.append(pythonPackage)

        return result

    def get_native_build_inputs(self) -> List:
        return self.get_poetry_deps("dev-dependencies")

    def get_propagated_build_inputs(self) -> List:
        return self.get_poetry_deps("dependencies")

    def get_build_inputs(self) -> List:
        return self.get_poetry_deps("dependencies")

    def get_optional_build_inputs(self) -> List:
        return self.get_poetry_deps("extras")

    def get_check_inputs(self) -> List:
        return self.get_poetry_deps("test")
