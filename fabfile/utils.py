'''
A grab bag of functions used by other modules
'''

import re
import os.path

from fabric.api import run, cd
from fabric.contrib.files import append, exists

import config


def rmdir(path, force=False):
    'Better than rm because it is silent when the file does not exist'
    flag = '-f' if force else ''
    if exists(path):
        run('rm {} -r {}'.format(flag, path))

def psql(command, connectionURI=''):
    with cd(config.paths['pg-latest']):
        return run('bin/psql {} -c "{}"'.format(connectionURI, command))

def add_github_to_known_hosts():
    'Removes prompts from github checkouts asking whether you want to trust the remote'
    key = 'github.com ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ=='
    append('/home/ec2-user/.ssh/known_hosts', key)

def download_pg():
    "Idempotent, does not download if file already exists. Returns the file's location"
    version = config.settings['pg-version']
    url = pg_url_for_version(version)

    target_dir = config.paths['pg-source-balls']
    run('mkdir -p {}'.format(target_dir))

    target_file = '{}/{}'.format(target_dir, os.path.basename(url))

    if exists(target_file):
        return target_file

    run('wget -O {} --no-verbose {}'.format(target_file, url))
    return target_file

def pg_url_for_version(version):
    return 'https://ftp.postgresql.org/pub/source/v{0}/postgresql-{0}.tar.bz2'.format(version)
