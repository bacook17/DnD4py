# -*- coding: utf-8 -*-

import os
import re
import codecs
from setuptools import setup, Command, find_packages
from setuptools.command.install import install

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


# https://packaging.python.org/guides/single-sourcing-package-version/
def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


class CleanCommand(Command):
    
    """Custom clean command to tidy up the project root.
    From https://stackoverflow.com/questions/3779915"""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


entry_points = {
    'console_scripts': ['lookup5e = DnD4py.lookup_5e:lookup',
                        'monster = DnD4py.lookup_5e:monster_lookup',
                        'spell = DnD4py.lookup_5e:spell_lookup',
                        'item = DnD4py.lookup_5e:item_lookup',
                        'roll = DnD4py.roll4me:roll',
                        ]
}

setup(
    name="DnD4py",
    version=find_version('DnD4py', '__init__.py'),
    install_requires=['numpy', 'bs4'],
    packages=find_packages(),
    entry_points=entry_points,
    author="Ben Cook",
    author_email="bacook17@gmail.com",
    description="Python Codes for DnD 5e",
    keywords="games, Dungeons and Dragons"
)
