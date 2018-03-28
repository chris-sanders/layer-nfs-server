from charmhelpers.core import hookenv


class NfsHelper():
    def __init__(self):
        self.charm_config = hookenv.config()
        self.exports_file = "/etc/exports"


