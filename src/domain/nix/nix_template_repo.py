from domain.nix.nix_template import NixTemplate
from domain.flake.recipe.flake_recipe import FlakeRecipe
from domain.repo import Repo

from typing import Dict

class NixTemplateRepo(Repo):
    """
    A subclass of Repo that manages nix templates.
    """

    def __init__(self):
        """
        Creates a new NixTemplateRepo instance.
        """
        super().__init__(NixTemplate)

    def find_flake_templates_by_recipe(self, recipe: FlakeRecipe) -> Dict[str, NixTemplate]:
        """Retrieves the flake templates associated to given recipe"""
        raise NotImplementedError(
            "find_flake_templates_by_recipe() must be implemented by subclasses"
        )
