#!/usr/bin/env python3
"""Decrypt SOPS files from within Python

This module can be used either as a library or a script.

Usage: sops.py [-v] [ --stage=<stage> | <file> ]
"""

import logging
import os
from pathlib import Path
import sys

from docopt import docopt
import sh


DM_CREDENTIALS_REPO = Path(os.environ["DM_CREDENTIALS_REPO"])
sops_wrapper = sh(_err=sys.stderr, _in=sys.stdin).sh.bake(DM_CREDENTIALS_REPO / "sops-wrapper")


def pre_auth():
    """Ask for MFA token"""
    sops_wrapper("-v")


def decrypt(fpath):
    """Decrypt a SOPS-encrypted file

    :param Path fpath: The file path
    :return: The decrypted contents
    :rtype: str
    :raises ValueError: if the file does not exist
    """
    if not fpath.is_file():
        raise ValueError(f"Expected a path to an existing file, but '{fpath}' is not a file or does not exist")
    return sops_wrapper("-d", fpath)


def get_secrets_for_stage(stage, decrypt=True):
    """Return the secrets for stage, optionally decrypted

    :param str stage: The stage to get secrets for, i.e. preview, staging, production
    :param bool decrypt: Whether to decrypt or not
    :return: The contents of the secrets file for the specified stage
    :rtype: str
    :raises ValueError: if the stage is not valid
    """
    fpath = DM_CREDENTIALS_REPO / "vars" / f"{stage}.yaml"
    if not fpath.is_file():
        raise ValueError(f"Expected a valid stage, but '{fpath}' does not exist")
    if decrypt:
        return decrypt(fpath)
    else:
        return fpath.read_text(encoding="utf8")


def main(argv=None):
    args = docopt(__doc__, argv=argv)
    if args["-v"]:
        logging.basicConfig(level=logging.INFO)
    if args["--stage"]:
        print(get_secrets_for_stage(args["--stage"]))
    elif args["<file>"]:
        print(decrypt(Path(args["<file>"])))
    else:
        pre_auth()


if __name__ == "__main__":
    main()
