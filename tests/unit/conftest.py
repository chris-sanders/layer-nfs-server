#!/usr/bin/python3
import pytest
import mock

import sys


# @pytest.fixture
# def cert(monkeypatch):
#     normal_open = open
#
#     def wrapper(*args, **kwargs):
#         content = None
#         if args[0] == '/etc/letsencrypt/live/mock/fullchain.pem':
#             content = 'fullchain.pem\n'
#             if 'b' in args[1]:
#                 content = bytes(content, encoding='utf8')
#         elif args[0] == '/etc/letsencrypt/live/mock/privkey.pem':
#             content = 'privkey.pem\n'
#             if 'b' in args[1]:
#                 content = bytes(content, encoding='utf8')
#         else:
#             file_object = normal_open(*args)
#             return file_object
#         file_object = mock.mock_open(read_data=content).return_value
#         file_object.__iter__.return_value = content.splitlines(True)
#         return file_object
#
#     monkeypatch.setattr('builtins.open', wrapper)


@pytest.fixture
def mock_layers():
    sys.modules["charms.layer"] = mock.Mock()
    sys.modules["reactive"] = mock.Mock()


@pytest.fixture
def mock_check_call(monkeypatch):
    mock_call = mock.Mock()
    monkeypatch.setattr('libnfs.subprocess.check_call', mock_call)
    return mock_call


@pytest.fixture
def mock_hookenv_config(monkeypatch):
    import yaml

    def mock_config():
        cfg = {}
        yml = yaml.load(open('./config.yaml'))

        # Load all defaults
        for key, value in yml['options'].items():
            cfg[key] = value['default']

        return cfg

    monkeypatch.setattr('libnfs.hookenv.config', mock_config)


@pytest.fixture
def nh(tmpdir, mock_layers, mock_hookenv_config, monkeypatch):
    from libnfs import NfsHelper
    nh = NfsHelper()

    # Set correct charm_dir
    monkeypatch.setattr('libnfs.hookenv.charm_dir', lambda: '.')

    # Patch the combined exports file to a tmpfile
    export_file = tmpdir.join("exports")
    nh.exports_file = export_file.strpath

    # Any other functions that load PH will get this version
    monkeypatch.setattr('libnfs.NfsHelper', lambda: nh)

    return nh
