#!/usr/bin/env python3

import logging
import logging.config

from subprocess import Popen
from typing import Optional

from lookyloo.default import get_config, get_homedir, AbstractManager

logging.config.dictConfig(get_config('logging'))


class Website(AbstractManager):

    def __init__(self, loglevel: Optional[int]=None):
        super().__init__(loglevel)
        self.script_name = 'website'
        self.process = self._launch_website()
        self.set_running()

    def _launch_website(self):
        website_dir = get_homedir() / 'website'
        ip = get_config('generic', 'website_listen_ip')
        port = get_config('generic', 'website_listen_port')
        return Popen(['gunicorn', '-w', '10',
                      '--graceful-timeout', '2', '--timeout', '300',
                      '-b', f'{ip}:{port}',
                      '--log-level', 'info',
                      'web:app'],
                     cwd=website_dir)


def main():
    w = Website()
    w.run(sleep_in_sec=10)


if __name__ == '__main__':
    main()
