#!/usr/bin/env python3
"""Decrypt SOPS files from within Python

This module can be used either as a library or a script.

Usage: sops.py [-v] [ --stage=<stage> | <file> ]
"""

import logging
import os
from pathlib import Path
import sys

from hashlib import sha1
import json

from docopt import docopt
from sh import aws, sops


AWS_PROFILE = "sops"
CACHE_DIR = Path.home() / ".aws" / "cli" / "cache"
DM_CREDENTIALS_REPO = Path(os.environ["DM_CREDENTIALS_REPO"])


def auth():
    """Get credentials for communicating with AWS as environment variables"""
    # We want to subsume the role of sops-wrapper and aws-auth
    aws_profile = os.getenv("AWS_PROFILE", AWS_PROFILE)

    def aws_configure_get(key, profile=aws_profile):
        return aws.configure.get(key, profile=profile).strip()

    aws.sts("get-caller-identity", _err=sys.stderr, _in=sys.stdin, _tty_in=True)
    source_profile = aws_configure_get("source_profile")
    role_arn = aws_configure_get("role_arn")
    mfa_serial = aws_configure_get("mfa_serial")

    def get_cache_file(role_arn, mfa_serial):
        key = {"RoleArn": role_arn, "SerialNumber": mfa_serial}
        plaintext = str(key).replace("'", '"').encode()
        digest = sha1(plaintext).hexdigest()
        return CACHE_DIR / f"{digest}.json"

    cache_file = get_cache_file(role_arn, mfa_serial)
    credentials = json.loads(cache_file.read_bytes())["Credentials"]

    environ = {
        "AWS_PROFILE": aws_profile,
        "AWS_DEFAULT_REGION": aws_configure_get("region", profile=source_profile),
        "AWS_ACCESS_KEY_ID": credentials["AccessKeyId"],
        "AWS_SECRET_ACCESS_KEY": credentials["SecretAccessKey"],
        "AWS_SECURITY_TOKEN": credentials["SessionToken"],
        "AWS_SESSION_TOKEN": credentials["SessionToken"],
    }

    return environ


def find_secrets_files(stage):
    """Return the path to the secrets file for the stage

    :param str stage: The stage to get secrets for, i.e. preview, staging, production
    :return: The path to the secrets file for the specified stage
    :rtype: Path
    :raises ValueError: if the stage is not valid
    """
    if not DM_CREDENTIALS_REPO.is_dir():
        raise RuntimeError(
            "Directory '{}' does not exist. Is the DM_CREDENTIALS_REPO environment variable set correctly?"
        )
    fpath = DM_CREDENTIALS_REPO / "vars" / f"{stage}.yaml"
    if not fpath.is_file():
        raise ValueError(f"Expected a valid stage, but '{fpath}' does not exist")
    return fpath


def decrypt(fpath):
    """Decrypt a SOPS-encrypted file

    :param Path fpath: The file path
    :return: The decrypted contents
    :rtype: dict or str
    :raises ValueError: if the file does not exist
    """
    if not fpath.is_file():
        raise ValueError(
            f"Expected a path to an existing file, but '{fpath}' is not a file or does not exist"
        )
    contents = sops("-d", fpath, _env=auth())
    if str(fpath).endswith(".yaml"):
        return yaml.safe_loads(contents)
    return contents


def main(argv=None):
    args = docopt(__doc__, argv=argv)
    auth()
    if args["-v"]:
        logging.basicConfig(level=logging.INFO)
    if args["--stage"]:
        print(get_secrets_for_stage(args["--stage"]))
    elif args["<file>"]:
        print(decrypt(Path(args["<file>"])))


if __name__ == "__main__":
    main()
