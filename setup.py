from distutils.core import setup
import os
import subprocess
__author__ = 'Aleksandr Vavilin'

if __name__ == '__main__':
    build = (('BUILD_NUMBER' in os.environ) and os.environ['BUILD_NUMBER'] or "M")
    branch = (('GIT_BRANCH' in os.environ) and os.environ['GIT_BRANCH'] or "")
    proc = subprocess.Popen(['git', 'rev-parse', '--short=8', 'HEAD'], stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    commit = stdout.strip()

    package_name = 'tbdd-pdm'
    versionstr = '0.1.{}-{}'.format(build, branch)
    fullversionstr = '0.1.{}-{} {}'.format(build, branch, commit)

    d = setup(
        name=package_name,
        version=versionstr,
        packages=[
            'tbdd_pdm_core',
            'tbdd_pdm_core.db',
            'tbdd_pdm_core.api',
            ],
        url='',
        license='',
        author='Aleksandr Vavilin',
        author_email='vavilin@tbdd.ru',
        description='Simple PDM for TBDD internal use', requires=['sqlalchemy', 'flask']
    )
