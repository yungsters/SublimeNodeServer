"""
SublimeNodeTextCommand.py
"""

import sublime_plugin

from .SublimeNodeServer import SublimeNodeServer # pylint: disable=F0401

class SublimeNodeTextCommand(sublime_plugin.TextCommand):
    """Forwards text commands to the node server."""

    def run(self, edit):
        SublimeNodeServer.thread.client.send("SublimeNodeTextCommand")
