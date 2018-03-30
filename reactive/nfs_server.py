from charms.reactive import (
    when_not,
    set_state,
    when,
)
from charmhelpers.core import (
    hookenv,
)
from charmhelpers import fetch

from libnfs import NfsHelper

nh = NfsHelper()


@when_not('nfs-server.installed')
def install_nfs_server():
    hookenv.status_set('maintenance', 'installing nfs server')
    fetch.apt_update()
    fetch.apt_install(['nfs-kernel-server'])
    nh.write_exports()
    hookenv.status_set('active', 'Nfs server is ready')
    set_state('nfs-server.installed')


@when('config.changed', 'nfs-server.installed')
def update_exports():
    nh.write_exports()
    hookenv.log("Exports file written", hookenv.INFO)
