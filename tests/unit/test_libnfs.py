#!/usr/bin/python3


class TestLibnfs():

    def test_pytest(self):
        assert True

    def test_nh(self, nh):
        ''' See if the nh fixture works to load charm configs '''
        assert isinstance(nh.charm_config, dict)

