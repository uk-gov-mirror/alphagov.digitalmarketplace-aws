#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import sys

import click

from .utils import load_file, template_string, merge_dicts, UndefinedError
from .variables import load_variables


TEMPLATES_DIR = Path("paas")


def app_manifest(environment, app, additional_variables=None):
    """Generate PaaS app manifest

    :param Environment environment: The environment to generate the manifest for
    :param str app: The app to generate the manifest for
    :return: the app manifest
    :rtype: str
    :raises ValueError: if the environment or app name are not valid
    """
    variables = load_defaults(environment, app)
    variables = merge_dict(variables, additional_variables or {})

    template_file = (TEMPLATES_DIR / f"{app}.j2")

    try:
        template_content = template_file.read_text()
    except FileNotFoundError:
        raise ValueError(f'app name "{app}" is not valid: path "{template_file}" does not exist')


    try:
        manifest_content = template_string(
            template_content, variables, templates_path=TEMPLATES_DIR
        )
    except UndefinedError as e:
        # the UndefinedError.message is usually something like "'VAR' is undefined"
        sys.exit(
            f"""Error: The template '{template_file}' thinks that the variable {e.message}."""
            """ Please check you have included all of the var files and command line vars that you need."""
        )


def get_variables_from_command_line_or_environment(vars):
    cli_vars = []
    for v in vars:
        # get (option, value) tuple from `--var` flag
        v = tuple(v.split("=", maxsplit=1))

        # if they didn't specify on the command line, check the envvars
        if len(v) == 1:
            v = (v[0], os.getenv(v[0]))
            if v[1] is None:
                raise KeyError(v[0])

        cli_vars.append(v)

    return dict(cli_vars)


@click.command()
@click.argument(
    "environment", nargs=1, type=click.Choice(["preview", "staging", "production"])
)
@click.argument("app", nargs=1)
@click.option(
    "--out-file",
    "-o",
    help="Output file, if empty the template content is printed to the stdout",
)
@click.option(
    "--vars-file",
    "-f",
    multiple=True,
    type=click.Path(exists=True),
    help="Load YAML or JSON variable file",
)
@click.option(
    "--var",
    "-v",
    multiple=True,
    type=str,
    help="Specify variables on the command line. "
    "Can be a key-value pair in the form option=value, "
    "or the name of an environment variable.",
)
def main(environment, app, vars_file, var, out_file):
    """Generate a PaaS manifest file from a Jinja2 template"""

    variables = {}

    for path in vars_file:
        variables = merge_dicts(variables, read_yaml_file(path))

    try:
        variables = get_variables_from_command_line_or_environment(var)
    except KeyError as e:
        sys.exit(
            f"""Error: Command line variable "--var '{e.args[0]}'" was not set by the flag"""
            """ and was not found in environment variables. Please check your environment is correctly configured."""
        )

    manifest_content = app_manifest(environment, app, additional_variables=variables)

    if out_file is not None:
        with open(out_file, "w") as f:
            f.write(manifest_content)
        os.chmod(out_file, 0o600)
    else:
        print(manifest_content)


if __name__ == "__main__":
    main()
