"""
SublimeNodeServer.py
"""

import getpass
import os
import platform
import socket
import subprocess
import sys
import time
import threading

import sublime

SERVER_ADDRESS = "/tmp/sublime-node-server.sock"
SERVER_PATH = os.path.join(
    sublime.packages_path(),
    os.path.dirname(os.path.realpath(__file__)),
    "SublimeNodeServer.js"
)

def plugin_loaded():
    """Called when the Sublime Text API is ready for use."""
    SublimeNodeServer.thread = SublimeNodeServer(SERVER_ADDRESS, SERVER_PATH)
    SublimeNodeServer.thread.start()

    SublimeNodeServer.thread.send("Hello...")
    SublimeNodeServer.thread.send("...world!")

def plugin_unloaded():
    """Called just before the plugin is unloaded."""
    if SublimeNodeServer.thread:
        SublimeNodeServer.thread.exit()

def get_node_paths():
    """Finds platform-specific node paths."""
    node_paths = []

    if platform.system() == 'Darwin':
        nvm_path = "/Users/{0}/.nvm".format(getpass.getuser())
        try:
            with open("{0}/alias/default".format(nvm_path), "r") as file:
                content = file.read()
            version = content.strip()
            node_path = "{0}/versions/node/v{1}/bin".format(nvm_path, version)
            node_paths.append(node_path)
        except FileNotFoundError:
            pass

    return node_paths

class SublimeNodeServer(threading.Thread):
    """Manages the node server."""

    thread = None

    def __init__(self, server_address, server_path):
        threading.Thread.__init__(self)
        self.server_address = server_address
        self.server_path = server_path
        self.child = None
        self.client = None
        self.queue = []

    def run(self):
        if os.path.exists(self.server_address):
            os.unlink(self.server_address)

        env = os.environ.copy()
        env["PATH"] += ''.join([':' + path for path in get_node_paths()])
        try:
            child = subprocess.Popen(
                ["node", self.server_path, self.server_address],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            self.child = child
        except OSError:
            raise Exception(
                "Couldn't find `node` in `{0}`.".format(env["PATH"])
            )

        self.client = self.connect()
        for (message, callback) in self.queue:
            self.send(message, callback)
        del self.queue[:]

        while child.poll() is None:
            stdout = child.stdout.readline().decode("utf-8")
            sys.stdout.write(stdout)

        stdout, stderr = child.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        if stdout:
            sys.stdout.write(stdout)
        if stderr:
            message = "Node server encountered an error.\n{0}".format(
                "\n".join(["> " + line for line in stderr.split("\n")])
            )
            raise Exception(message)

    def connect(self):
        """Connects to the node server."""
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        end_time = time.time() + 10
        while True:
            remaining_time = end_time - time.time()
            if remaining_time < 0:
                raise Exception(
                    "Unable to connect to `{0}`".format(self.server_address)
                )
            try:
                client.connect(self.server_address)
                break
            except (ConnectionRefusedError, FileNotFoundError):
                time.sleep(0.1)

        return client

    def send(self, message, callback=None):
        """Sends a message to the node server."""
        if self.client:
            encoded = sublime.encode_value(message) + "\n"
            self.client.send(bytes(encoded, "utf-8"))
            if callback:
                callback()
        else:
            self.queue.append((message, callback))

    def exit(self):
        """Sends SIGINT to the node child process."""
        if self.child.poll() is None:
            self.child.terminate()
