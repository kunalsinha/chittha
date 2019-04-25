from setuptools import setup, find_packages
import os, glob

def readfile(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read()

setup(
    name = 'chittha',
    version = '1.0',
    author = 'Kunal Sinha',
    author_email = 'kunalsinha4u@gmail.com',
    description = 'Sticky notes application',
    long_description = readfile('README.md'),
    packages = ['chittha', 'resources'],
    package_data = {
        'resources': ['*.png'],
    },
    install_requires = ['PyQt5==5.12.1'],
    python_requires = '>=3',
    data_files = [
        ('/usr/share/applications', ('app/chittha.desktop', )),
        ('/usr/share/pixmaps', ('app/chittha.svg', )),
    ],
    #scripts = ['main.py',],
    entry_points = {
        'gui_scripts': [
            'chittha = chittha.engine:Engine.start',
        ]
    },
    license = 'GPL 3',
    keywords = 'sticky note notes reminder chittha',
    url = 'https://github.com/kunalsinha/chittha',
    classifiers = [
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ]
    #project_urls = {
    #    "Bug Tracker": "https://bugs.example.com/chittha/",
    #    "Documentation": "https://docs.example.com/chittha/",
    #    "Source Code": "https://code.example.com/chittha/",
    #}
)

