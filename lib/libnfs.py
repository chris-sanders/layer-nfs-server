import subprocess

from charmhelpers.core import (
    hookenv,
    templating,
)


class NfsHelper():
    def __init__(self):
        self.charm_config = hookenv.config()
        self.exports_file = "/etc/exports"

    def write_exports(self):
        context = {}
        for entry in self.charm_config.keys():
            context[entry.replace('-', '_')] = str(self.charm_config[entry])
        templating.render('exports', self.exports_file, context)
        subprocess.check_call('exportfs -ra')
