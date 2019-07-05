import pytest

from pathlib import Path
from unittest.mock import call, patch

import deploy_tools.variables


@pytest.fixture(autouse=True)
def read_yaml_file():
    with patch("deploy_tools.variables.read_yaml_file", return_value={}) as mock:
        yield mock


@pytest.fixture(autouse=True)
def vars_dir(tmpdir):
    vars_dir = Path(tmpdir, "deploy_tools", "vars")
    with patch("deploy_tools.variables.VARS_DIR", vars_dir) as path:
        yield path


@pytest.fixture(autouse=True)
def secrets_dir(tmpdir):
    dm_credentials_repo = Path(tmpdir, "dm_credentials_repo")
    secrets_dir = dm_credentials_repo / "vars"
    with patch(
        "deploy_tools.variables.DM_CREDENTIALS_REPO", dm_credentials_repo
    ) as path:
        yield secrets_dir


@pytest.fixture(autouse=True)
def path_is_file():
    with patch("deploy_tools.variables.Path.is_file", return_value=True) as mock:
        yield mock


def test_load_defaults_gets_all_the_vars_and_secrets_files(
    read_yaml_file, sops_decrypt, vars_dir, secrets_dir
):
    deploy_tools.variables.load_defaults("testing")

    expected = [
        call(vars_dir / "common.yml"),
        call(vars_dir / "testing.yml"),
        call(vars_dir / "users.yml"),
        call(secrets_dir / "testing.yaml"),
    ]
    got = read_yaml_file.call_args_list + sops_decrypt.call_args_list

    assert got == expected


def test_load_defaults_common_variables_are_always_loaded_first_before_specific_variables(
        read_yaml_file, sops_decrypt, vars_dir
):
    # use a single call_args_list
    sops_decrypt.call_args_list = read_yaml_file.call_args_list
    deploy_tools.variables.load_defaults("testing")
    assert read_yaml_file.call_args_list == sops_decrypt.call_args_list
    assert read_yaml_file.call_args_list[0] == call(vars_dir / "common.yml")


def test_load_defaults_returns_a_merged_dict_of_variables(read_yaml_file, sops_decrypt, vars_dir, secrets_dir):
    files = lambda path: {
            vars_dir / "common.yml": {"a": "alpha"},
            vars_dir / "testing.yml": {"b": "beta"},
            vars_dir / "users.yml": {"g": "gamma"},
            secrets_dir / "testing.yaml": {"key": "my-super-secret-password"},
    }[path]

    read_yaml_file.side_effect = files
    sops_decrypt.side_effect = files

    assert deploy_tools.variables.load_defaults("testing") == {
        "a": "alpha",
        "b": "beta",
        "g": "gamma",
        "key": "my-super-secret-password",
        "environment": "testing",
    }


@pytest.mark.parametrize("environment", ("testing", "production"))
def test_load_defaults_always_includes_the_environment_in_output(environment):
    assert deploy_tools.variables.load_defaults(environment)["environment"] == environment


def test_load_defaults_raises_value_error_if_environment_is_invalid(path_is_file):
    path_is_file.return_value = False
    expected_message = r'invalid environment "foobar": file ".*" does not exist'
    with pytest.raises(ValueError, match=expected_message) as e:
        deploy_tools.variables.load_defaults("foobar")


@pytest.mark.parametrize("load_default_files", (True, False))
@patch("deploy_tools.variables.load_defaults", autospec=True, return_value={})
def test_load_variables_calls_loads_defaults_if_load_default_files_is_true(
    load_defaults, load_default_files
):
    deploy_tools.variables.load_variables(
        "testing", load_default_files=load_default_files
    )
    assert load_defaults.called == load_default_files


def test_load_variables_loads_other_var_files(read_yaml_file, sops_decrypt):
    deploy_tools.variables.load_variables(
        "testing", vars_files=["foo", "bar", "baz"], load_default_files=False
    )
    assert read_yaml_file.call_args_list == [call("foo"), call("bar"), call("baz")]
