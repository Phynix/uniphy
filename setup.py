# -*- coding: utf-8 -*-
"""
Setup of uniphy
"""

from setuptools import setup

import io
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(current_dir, 'requirements.txt')) as f:
    requirements = f.read().split('\n')


def readme():
    """Open README.md, read the file and return it as a string"""
    with open('README.md') as readme:
        return readme.read()


setup(name='uniphy',
      version='0.0.2',  # TODO: automatise versioning
      description='Unification and collection of algorithms used in physics',
      long_description=readme(),
      classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Natural Language :: English',
          'Operating System :: MacOS',
          'Operating System :: MacOS :: MacOS 9',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Unix',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Scientific/Engineering :: Physics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Mathematics'
      ],
      keywords='physics, analysis, algorithm',
      url='https://github.com/Phynix/uniphy',
      author='Jonas Eschle',
      author_email='mayou36@jonas.eschle.com',
      license='GNU Lesser General Public License v3',
      # dependency_links="",
      install_requires=requirements,
      # extras_require=,
      packages=['uniphy'],
      include_package_data=True,
      zip_safe=False
      )
