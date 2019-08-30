from codecs import open
import os
from setuptools import setup
from routeros_updates import __VERSION__


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r') as infile:
    long_description = infile.read()


setup(
    name='routeros-updates',
    version=__VERSION__,
    packages=['routeros_updates'],
    url='https://github.com/phistrom/routeros-updates',
    license='MIT',
    author='Phillip Stromberg',
    author_email='phillip@strombergs.com',
    description='RouterOS Update Checker and Downloader',
    entry_points={
        'console_scripts': ['ros-updates=routeros_updates:cli']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown"
)
