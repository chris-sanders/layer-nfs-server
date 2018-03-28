from charms.reactive import (
    when_not, set_state
    # when, when_not, set_state
)
from charmhelpers.core import (
    # host,
    hookenv,
)
from charmhelpers import fetch

from libnfs import NfsHelper

nh = NfsHelper()


@when_not('nfs-server.installed')
def install_nfs_server():
    hookenv.status_set('maintenance', 'installing nfs server')
    fetch.auto_update()
    fetch.apt_install(['nfs-kernel-server'])
    set_state('nfs-server.installed')


