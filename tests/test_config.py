import re
import shutil

import pytest

from src.utility import load_config


def test_exception_if_missing_config_file(mocker):
    missing_config_file = "missing_config.yaml"
    with pytest.raises(FileNotFoundError, match=f"Specified configuration file {missing_config_file} does not exist"):
        load_config(missing_config_file)


def test_load_default_config_file(mocker):
    # Test to ensure that a call to load_config returns a dictionary with the correct
    # number of entries for the default configuration
    config = load_config(None)
    assert config is not None
    assert len(config.__dict__) == 22


def test_load_user_config_file(mocker):
    user_config_file = "input/user_config.yaml"
    config = load_config(user_config_file)
    assert config is not None
    assert len(config.__dict__) == 22


def test_load_empty_config_file(tmp_path):
    empty_config_file = tmp_path / "empty_config_file.yaml"
    open(empty_config_file, "w").close()
    assert load_config(empty_config_file) is not None


def test_load_invalid_config_file(tmp_path):
    invalid_config_file = tmp_path / "invalid_config_file.yaml"
    shutil.copy("../readme.md", invalid_config_file)
    with pytest.raises(RuntimeError,
                       match=re.escape(
                           f"Invalid YAML in {invalid_config_file}.  Please verify syntax of YAML content."
                       )):
        load_config(invalid_config_file)
