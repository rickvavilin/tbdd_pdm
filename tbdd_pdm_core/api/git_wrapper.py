import os
import subprocess
import datetime
import dateutil.parser
__author__ = 'Aleksandr Vavilin'

LOG_HEADERS = (
    'rev',
    'author',
    'datetime',
    'comment'
)

def add_file(path, git_root_path=None, committer_name=None, committer_email=None, comment=''):
    env = os.environ
    env['GIT_AUTHOR_NAME'] = committer_name
    env['GIT_AUTHOR_EMAIL'] = committer_email
    env['GIT_COMMITTER_NAME'] = committer_name
    env['GIT_COMMITTER_EMAIL'] = committer_email
    env['GIT_DIR'] = os.path.join(git_root_path, '.git')
    env['GIT_WORK_TREE'] = git_root_path
    print(git_root_path, path)
    p = subprocess.Popen(['git', 'add', path], env=env, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception(stderr)
    p = subprocess.Popen(['git', 'commit', '-m', comment, '--allow-empty'], env=env, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception(stdout+stderr)


def gelete_file(path, git_root_path=None, committer_name=None, committer_email=None, comment=''):
    env = os.environ
    env['GIT_AUTHOR_NAME'] = committer_name
    env['GIT_AUTHOR_EMAIL'] = committer_email
    env['GIT_COMMITTER_NAME'] = committer_name
    env['GIT_COMMITTER_EMAIL'] = committer_email

    env['GIT_DIR'] = os.path.join(git_root_path, '.git')
    env['GIT_WORK_TREE'] = git_root_path
    p = subprocess.Popen(['git', 'rm', '-f', path], env=env, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception(stderr)
    p = subprocess.Popen(['git', 'commit', '-m', comment], env=env, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception(stdout+stderr)


def get_file_history(path, git_root_path=None):
    env = os.environ
    env['GIT_DIR'] = os.path.join(git_root_path, '.git')
    env['GIT_WORK_TREE'] = git_root_path
    p = subprocess.Popen(['git', 'log', '--pretty=format:%h|%an|%ad|%s', '--date=iso-strict', '--', path], env=env, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception(stderr)
    stdout = stdout.decode('utf8')
    log = [dict(zip(LOG_HEADERS, l.split('|'))) for l in stdout.split('\n')]
    for l in log:
        l['datetime'] = dateutil.parser.parse(l['datetime'])
    return log


