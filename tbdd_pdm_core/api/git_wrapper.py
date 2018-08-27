import os
import subprocess
__author__ = 'Aleksandr Vavilin'


def add_file(path, committer_name=None, committer_email=None, comment=''):
    env = os.environ
    env['GIT_AUTHOR_NAME'] = committer_name
    env['GIT_AUTHOR_EMAIL'] = committer_email
    p = subprocess.Popen(['git', 'add', path], env=env, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception(stderr)
    p = subprocess.Popen(['git', 'commit', '-m', comment], env=env, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception(stderr)


def gelete_file(path, committer_name=None, committer_email=None, comment=''):
    env = os.environ
    env['GIT_AUTHOR_NAME'] = committer_name
    env['GIT_AUTHOR_EMAIL'] = committer_email
    p = subprocess.Popen(['git', 'rm', '-f', path], env=env, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception(stderr)
    p = subprocess.Popen(['git', 'commit', '-m', comment], env=env, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception(stderr)


