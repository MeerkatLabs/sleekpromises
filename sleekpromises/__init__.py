from sleekxmpp.plugins.base import register_plugin as _register_plugin

from sleekpromises.scheduler import sleekpromises_scheduler as _scheduler


def register_sleek_promises():
    """
    Register the sleek promises components for the sleek xmpp framework.
    :return:
    """
    _register_plugin(_scheduler)
