import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    subprocess.call(['python', 'setup.py', 'sdist', 'upload', '--sign'])
    sys.exit()

README = open('README.md').read()
LICENSE = open("LICENSE").read()
VERSION = open("version").read().strip()

print VERSION

sys.exit()

setup(
    name='jirainfo',
    version=(VERSION),
    long_description=(README),
    author='Sebastian Ruml',
    author_email='sebastian@sebastianruml.name',
    py_modules=['termui'],
    include_package_data=True,
    install_requires=[
        'click',
        'Jinja2',
        'jira',
        # Colorama is only required for Windows.
        'colorama',
        'prettytable'
    ],
    license=(LICENSE),
    packages=['jirainfo'],
    scripts=['bin/jira-info']
)
