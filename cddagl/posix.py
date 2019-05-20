import errno
import fcntl
import os
from time import sleep


class SingleInstance:
    def __init__(self):
        self.run_once_fd = open(os.path.realpath(__file__), 'r')
        self.is_already_running = False
        try:
            fcntl.flock(self.run_once_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.is_already_running = True

    def aleradyrunning(self):
        return self.is_already_running

    def close(self):
        fcntl.flock(self.run_once_fd, fcntl.LOCK_UN)

    def __del__(self):
        self.close()


def get_ui_locale():
    return os.getenv('LANG')


class PyWinError(Exception):
    """
    Dummy class
    """
    pass


class SimpleNamedPipe:
    def __init__(self, name):
        self.name = name
        self.fifo = None
        self.fd = None
        self.create_pipe()

    def create_pipe(self):
        self.fifo = './pipe/{name}'.format(name=self.name)
        try:
            os.mkfifo(self.fifo)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                raise

    def connect(self):
        try:
            self.fd = open(self.fifo)
            return self.fd
        except IOError as e:
            if self.fifo is not None:
                os.unlink(self.fifo)
            self.create_pipe()
            self.fd = open(self.fifo)
            return self.fd

    def read(self, size):
        data = self.fd.read(size)
        if len(data) == 0:
            # pipe closed
            raise IOError("Pipe closed")

        return data

    def close(self):
        if self.fd:
            self.fd.close()
            self.fifo.unlink()
            self.fifo = None

    def __del__(self):
        self.close()


def process_id_from_path(path):
    import glob
    for pid_path in glob.glob('/proc/[0-9]*/'):
        # cmdline represents the command whith which the process was started
        if os.access(pid_path, os.R_OK):
            exe_link = "{}/exe".format(pid_path)
            if os.access(exe_link, os.R_OK):
                if os.path.realpath(os.readlink(exe_link)) == path:
                    return pid_path.split("/")[2]
    return None


def wait_for_pid(pid):
    # On Linux there is no way to cleanly wait for a non-child process to
    # finish executing without some sort of busy loop.

    f = '/proc/{}/exe'.format(pid)

    if not os.path.isfile(f):
        return False

    while os.path.isfile(f):
        sleep(3)

    return True
