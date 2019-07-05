import pytest

from pathlib import Path
from unittest.mock import call, patch

import deploy_tools.variables


@pytest.fixture(autouse=True)
def sops_decrypt():
    with patch("deploy_tools.variables.decrypt", return_value={}) as mock:
        yield mock


@pytest.fixture(autouse=True)
def read_yaml_file():
    with patch("deploy_tools.variables.read_yaml_file", return_value={}) as mock:
        yield mock


@pytest.fixture(autouse=True)
def vars_dir(tmpdir):
    vars_dir = Path(tmpdir, "deploy_tools", "vars")
    vars_dir.mkdir(parents=True, exist_ok=True)
    (vars_dir / "common.yml").write_text("a: alpha\n")
    (vars_dir / "testing.yml").write_text("b: beta\n")
    with patch("deploy_tools.variables.VARS_DIR", vars_dir) as path:
        yield path


@pytest.fixture(autouse=True)
def secrets_dir(tmpdir):
    dm_credentials_repo = Path(tmpdir, "dm_credentials_repo")
    secrets_dir = dm_credentials_repo / "vars"
    secrets_dir.mkdir(parents=True, exist_ok=True)
    (secrets_dir / "testing.yaml").write_text("key: my-super-secret-password\n")
    with patch(
        "deploy_tools.variables.DM_CREDENTIALS_REPO", dm_credentials_repo
    ) as path:
        yield secrets_dir


def test_load_defaults_gets_all_the_vars_and_secrets_files(
    read_yaml_file, sops_decrypt, vars_dir, secrets_dir
):
    deploy_tools.variables.load_defaults("testing")

    expected = [
        call(vars_dir / "common.yml"),
        call(vars_dir / "testing.yml"),
        call(secrets_dir / "testing.yaml"),
    ]
    got = read_yaml_file.call_args_list + sops_decrypt.call_args_list

    assert got == expected


def test_load_defaults_common_variables_are_always_loaded_first_before_specific_variables(
    read_yaml_file, vars_dir
):
    # use a single call_args_list
    sops_decrypt.call_args_list = read_yaml_file.call_args_list
    deploy_tools.variables.load_defaults("testing")
    assert read_yaml_file.call_args_list == sops_decrypt.call_args_list
    assert read_yaml_file.call_args_list[0] == call(vars_dir / "common.yml")


def test_load_defaults_returns_a_merged_dict_of_variables(read_yaml_file, sops_decrypt):
    read_yaml_file.side_effect = deploy_tools.utils.read_yaml_file
    sops_decrypt.side_effect = deploy_tools.utils.read_yaml_file

    assert deploy_tools.variables.load_defaults("testing") == {
        "a": "alpha",
        "b": "beta",
        "key": "my-super-secret-password",
    }


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
