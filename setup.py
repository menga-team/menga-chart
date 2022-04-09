import pathlib
from os.path import join
import sys

from  menga_chart import *

from setuptools import setup, find_packages
here = pathlib.Path(__file__).parent.resolve()
readme = open(join(here,'README.md')).read()

setup(
        name=name,
        version=version,
        url=url,
        license=license,
        author=version,
        author_email=email,
        description=description,
        long_description=readme,
        long_description_content_type='text/markdown',
        install_requires=['certifi', 'charset-normalizer', 'idna', 'numpy', 'PyQt5', 'PyQt5-Qt5', 'PyQt5-sip', 'pyqtgraph', 'PyYAML', 'qtwidgets', 'requests', 'urllib3'],
        entry_points='''
            [console_scripts]
            menga-chart=menga_chart.main:main
        ''',
        packages=find_packages()
        # packages = ["menga_chart"],
        # packages=find_packages(where="src", include="menga_chart")
)