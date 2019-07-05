"""Variables, parameters and secrets for the Digital Marketplace apps

This module should be the only one you need if you want to get configuration
values for Digital Marketplace apps. It knows where the config files are and
how to read them, including those in the digitalmarketplace-credentials repo.
It uses the `sops` module to decrypt secrets.
"""
from enum import Enum
from os import environ
from pathlib import Path
import sys

from .sops import decrypt
from .utils import merge_dicts, read_yaml_file


VARS_DIR = Path("vars")
DM_CREDENTIALS_REPO = None

try:
    DM_CREDENTIALS_REPO = Path(environ["DM_CREDENTIALS_REPO"]).resolve(strict=True)
except KeyError:
    print(
        "environment variable DM_CREDENTIALS_REPO is not set. Secrets will not be included in variables",
        file=sys.stderr,
    )
except FileNotFoundError:
    print(
        f"""is the environment variable DM_CREDENTIALS_REPO set correctly? "{DM_CREDENTIALS_REPO}" is not a directory. Secrets will not be included in variables""",
        file=sys.stderr,
    )


# Let's define our terms
class Space(Enum):
    """A PaaS space in the digitalmarketplace org"""

    preview = "preview"
    staging = "staging"
    production = "production"
    monitoring = "monitoring"


class Environment(Enum):
    """One of the systems where we can run Digital Marketplace code"""

    local = "development"
    development = "development"
    preview = "preview"
    staging = "staging"
    production = "production"


def load_variables(
    environment, vars_files=None, variables=None, load_default_files=True
):
    variables = variables or {}
    if load_default_files:
        variables = merge_dicts(variables, load_defaults(environment))
    for path in vars_files or []:
        variables = merge_dicts(variables, read_yaml_file(path))

    return variables


def load_defaults(environment):
    """Return the default variables for the environment

    :param Environment environment: The environment to get variables for
    :returns: the variables
    :rtype: dict
    :raises ValueError: if environment is not valid
    """
    vars_files = [VARS_DIR / "common.yml", VARS_DIR / f"{environment}.yml"]
    secrets_files = (
        [DM_CREDENTIALS_REPO / "vars" / f"{environment}.yaml"]
        if DM_CREDENTIALS_REPO
        else []
    )

    if (VARS_DIR / "users.yml").is_file():
        vars_files.append(VARS_DIR / "users.yml")

    for path in vars_files + secrets_files:
        if not path.is_file():
            raise ValueError(
                'invalid environment "{environment}" (file "{path}" does not exist)'
            )

    variables = {}
    for path in vars_files:
        variables = merge_dicts(variables, read_yaml_file(path))
    for path in secrets_files:
        variables = merge_dicts(variables, decrypt(path))

    return variables
