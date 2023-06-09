from domain.flake.flake_requested import FlakeRequested
from domain.primary_port import PrimaryPort

import argparse
import logging

class CreateFlakeCli(PrimaryPort):

    """
    A PrimaryPort that emits FlakeRequested events specified from the command line.
    """
    def __init__(self):
        super().__init__()

    def priority(self) -> int:
        return 100

    async def accept(self, app):

        parser = argparse.ArgumentParser(description="Generates a flake for a given Python package")
        parser.add_argument("command", choices=['create', 'build'], nargs='?', default=None, help="Whether to generate a nix flake")
        parser.add_argument("packageName", help="The name of the Python package")
        parser.add_argument("packageVersion", help="The version of the Python package")
        # TODO: Check how to avoid including flags from other cli handlers such as the following
        parser.add_argument("-t", "--github_token", required=False, help="The github token")
        parser.add_argument("-f", "--flakes_folder", required=False, help="The flakes folder")
        parser.add_argument("-u", "--flakes_url", required=False, help="The flakes url")
        parser.add_argument(
            "-x", "--forensic_folder", required=False, help="The folder where to copy the contents of flakes whose build failed"
        )
        args, unknown_args = parser.parse_known_args()

        if args.command == 'create':

            event = FlakeRequested(args.packageName, args.packageVersion, args.flakes_folder)
            logging.getLogger(__name__).debug(f'Emitting {event}')
            await app.acceptFlakeRequested(event)
