from __future__ import unicode_literals
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import logging
import sys

from . import constants, operations


log = logging.getLogger("routeros_update_check")

_subparser_required = sys.version_info >= (3, 7)  # in 3.7, argparse now


def cli():
    parser = ArgumentParser(description=constants.CLI_DESCRIPTION, epilog=constants.CLI_EXAMPLES,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("--channel", choices=constants.LATEST_CHANNEL_URL.keys(),
                        default="stable", help="Release channel to use. Defaults to 'stable'")
    parser.add_argument("--nossl", action="store_true", help="Use regular HTTP instead of HTTPS")
    parser.add_argument("-v", "--verbose", action="store_true", help="Output debug messages too.")

    subparser_params = {"dest": "action", "title": "actions"}
    if _subparser_required:
        subparser_params["required"] = True
    actions = parser.add_subparsers(**subparser_params)

    download_parser = actions.add_parser("download", help="Download the update to a given file location.")
    download_parser.add_argument("arch", choices=constants.ARCHITECTURES,
                                 help="Which architecture to download the packages for")
    download_parser.add_argument("--file", default="./", metavar="file", dest="path",
                                 help="Where to download the update to. By default the file is downloaded "
                                      "to the current directory.")
    download_parser.add_argument("--package", choices=["main", "all"], default="main",
                                 help="Download the main RouterOS package or all the optional packages. By default "
                                      "the main package is downloaded.")
    download_parser.add_argument("-f", "--force", action="store_true",
                                 help="Overwrite existing file")

    url_parser = actions.add_parser("url", help="Returns the HTTP download URL for the update")
    url_parser.add_argument("arch", choices=constants.ARCHITECTURES,
                            help="Which architecture to download the packages for")
    url_parser.add_argument("--package", choices=["main", "all"], default="main",
                            help="Specify whether to return the URL for the main package or all optional packages.")

    notes_parser = actions.add_parser("notes", help="Returns the patch notes for this update")

    args = parser.parse_args()

    return _perform_action(args)


def _perform_action(args):
    log.debug(args)
    d = args.__dict__.copy()
    action = d.pop("action")
    verbose = d.pop("verbose")
    nossl = d.pop("nossl")

    d["scheme"] = "http" if nossl else "https"

    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    result = {
        "notes": operations.get_patch_notes,
        "url": operations.get_download_url,
        "download": operations.download_file
    }[action](**d)

    return result
