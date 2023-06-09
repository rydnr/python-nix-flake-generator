from domain.flake.build.build_flake_requested import BuildFlakeRequested
from domain.primary_port import PrimaryPort

import argparse
import logging


class BuildFlakeCli(PrimaryPort):

    """
    A PrimaryPort that sends BuildFlake commands specified from the command line.
    """
    def priority(self) -> int:
        return 100

    async def accept(self, app):

        parser = argparse.ArgumentParser(
            description="Builds a given flake"
        )
        parser.add_argument("command", choices=['create', 'build'], nargs='?', default=None, help="Whether to generate a nix flake")
        parser.add_argument("packageName", help="The name of the Python package")
        parser.add_argument("packageVersion", help="The version of the Python package")
        parser.add_argument(
            "-f", "--flakes_folder", required=False, help="The folder containing the flakes"
        )
        # TODO: Check how to avoid including flags from other cli handlers such as the following
        parser.add_argument(
            "-t", "--github_token", required=False, help="The github token"
        )
        parser.add_argument("-u", "--flakes_url", required=False, help="The flakes url")
        parser.add_argument(
            "-x", "--forensic_folder", required=False, help="The folder where to copy the contents of flakes whose build failed"
        )
        args, unknown_args = parser.parse_known_args()

        if args.command == "build":
            event = BuildFlakeRequested(args.packageName, args.packageVersion, args.flakes_folder)
            logging.getLogger(__name__).debug(f"Requesting the building of flake {event.package_name}-{event.package_version} to {app}")
            await app.accept(event)
