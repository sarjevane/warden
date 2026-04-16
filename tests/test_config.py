"""Testing lib/config"""

import pytest
from pydantic import ValidationError

from warden.lib.config.config import Config, SchedulerConfig
from warden.lib.config.config import SchedulerConfig, UsersConfig


def test_scheduler():
    with pytest.raises(ValidationError):
        SchedulerConfig(strategy="NOT_FIFO", db_polling_interval_s=1)


def test_config_env_vars_use_warden_prefix(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("WARDEN_API_HOST", "127.0.0.1")
    monkeypatch.setenv("API_HOST", "192.0.2.10")

    config = Config()

    assert config.api.host == "127.0.0.1"


def test_unprefixed_env_vars_do_not_override_config(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("API_HOST", "127.0.0.1")

    config = Config()

    assert config.api.host == "0.0.0.0"
def test_authorized_list():
    """
    Test that authorized_list is a list of strings
    coerced from user inputs
    """
    config = UsersConfig(authorized_list=[1000, "2000"])
    assert "1000" in config.authorized_list
    assert "2000" in config.authorized_list
    assert 1000 not in config.authorized_list


def test_authorized_list_wrong_input():
    """
    Test that authorized_list is a list of strings
    coerced from user inputs that must be either strings or integers
    """
    with pytest.raises(ValidationError):
        UsersConfig(authorized_list=[[]])

    with pytest.raises(ValidationError):
        UsersConfig(authorized_list=[1.0])
