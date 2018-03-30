#!/usr/bin/python3


class TestLibnfs():

    def test_pytest(self):
        assert True

    def test_nh(self, nh):
        ''' See if the nh fixture works to load charm configs '''
        assert isinstance(nh.charm_config, dict)

    def test_write_exports(self, nh, mock_check_call):
        nh.write_exports()
        # Check default file is blank
        with open(nh.exports_file, 'r') as exports:
            assert exports.read() == "# This file is managed by the nfs-server charm edits will not persist\n\n"
        # Check with one share
        nh.charm_config['nfs-shares'] = '/mnt/tst'
        nh.write_exports()
        with open(nh.exports_file, 'r') as inFile:
            exports = inFile.read()
            assert "/mnt/tst\t*(rw,sync,no_subtree_check)" in exports
        # Check with multiple shares
        nh.charm_config['nfs-shares'] = '/mnt/tst,/mnt/tst2'
        nh.write_exports()
        with open(nh.exports_file, 'r') as inFile:
            exports = inFile.read()
            assert "/mnt/tst\t*(rw,sync,no_subtree_check)" in exports
            assert "/mnt/tst2\t*(rw,sync,no_subtree_check)" in exports
        # Check with custom client
        nh.charm_config['nfs-clients'] = "192.168.0.0/23"
        nh.write_exports()
        with open(nh.exports_file, 'r') as inFile:
            exports = inFile.read()
            assert "/mnt/tst\t192.168.0.0/23(rw,sync,no_subtree_check)" in exports
            assert "/mnt/tst2\t192.168.0.0/23(rw,sync,no_subtree_check)" in exports
        # Check with multiple clients
        nh.charm_config['nfs-clients'] = "192.168.0.0/23,10.0.0.0/23"
        nh.write_exports()
        with open(nh.exports_file, 'r') as inFile:
            exports = inFile.read()
            assert "/mnt/tst\t192.168.0.0/23(rw,sync,no_subtree_check)" in exports
            assert "/mnt/tst2\t192.168.0.0/23(rw,sync,no_subtree_check)" in exports
            assert "/mnt/tst\t10.0.0.0/23(rw,sync,no_subtree_check)" in exports
            assert "/mnt/tst2\t10.0.0.0/23(rw,sync,no_subtree_check)" in exports
        # Check with custom line
        nh.charm_config['nfs-custom'] = "/mnt/custom\tbob(rw,async)"
        nh.write_exports()
        with open(nh.exports_file, 'r') as inFile:
            exports = inFile.read()
            assert "/mnt/custom\tbob(rw,async)" in exports
        # Check with multiple custom lines
        nh.charm_config['nfs-custom'] = "/mnt/custom\tbob(rw,async);/mnt/custom\ttom(rw,async)"
        nh.write_exports()
        with open(nh.exports_file, 'r') as inFile:
            exports = inFile.read()
            assert "/mnt/custom\tbob(rw,async)" in exports
            assert "/mnt/custom\ttom(rw,async)" in exports
        # Verify file was reloaded after each write
        assert mock_check_call.call_count == 7
