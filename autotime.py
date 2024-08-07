from __future__ import print_function
from IPython.core.magics.execution import _format_time as fmt
import os

NOTIFICATION_MSG = u"terminal-notifier -appIcon https://www.python.org/static/apple-touch-icon-144x144-precomposed.png -sound Submarine -message '\u23F1 {}' -title '{} \u2714'"
__version__ = '0.1'

try:
    from time import perf_counter
except ImportError:
    from time import time as perf_counter


class Timer(object):
    def __init__(self, thresholds=(0.1, 10.0)):
        """
        Timer is a simple class to keep track of elapsed time.

        Parameters
        ----------
        thresholds : float
            Any times below the first threshold (in seconds) are not printed
            Times greater than the second threshold are shown as a desktop notification
        """
        self.start_time = 0.0
        self.theta_print = thresholds[0]
        self.theta_display = thresholds[1]

    def start(self, result):
        """Start the timer"""
        del result  # Unused.
        self.start_time = perf_counter()

    def stop(self, result):
        """Stops the timer, and prints the elapsed time"""

        if self.start_time:
            diff = perf_counter() - self.start_time

            # print to terminal if greater than the first threshold
            if diff > self.theta_print:
                print(u'\u23F1  {}'.format(fmt(diff)))

            # Use terminal-notifier to provide a desktop notification.
            if diff > self.theta_display and os.uname().sysname == 'Darwin':
                msg = NOTIFICATION_MSG.format(fmt(diff), result.info.raw_cell)
                os.system(msg)


def load_ipython_extension(ip):
    """On load, start and stop the timer every time a cell is run"""
    ip.events.register('pre_run_cell', timer.start)
    ip.events.register('post_run_cell', timer.stop)


def unload_ipython_extension(ip):
    """On unload, remove the timer"""
    ip.events.unregister('pre_run_cell', timer.start)
    ip.events.unregister('post_run_cell', timer.stop)


timer = Timer()
