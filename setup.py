from distutils.core import setup

# read the contents of your README file
from os import path
folder_path = path.abspath(path.dirname(__file__))
with open(path.join(folder_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = 'v0.0.3'

setup(
  name = 'PyPlaque',
  packages = ['PyPlaque'],
  version = version,
  license='GPLv3',
  description = 'Python package for virus plaque analysis based on Plaque2.0',
  author = 'Plaque2.0 Team, AILS Institute',
  author_email = 'ayakimovich@ails.institute',
  url = 'https://github.com/plaque2/PyPlaque',
  download_url = 'https://github.com/plaque2/PyPlaque/archive/{}.tar.gz'.format(version),
  keywords = ['Virus', 'Plaque', 'Virology', 'Microscopy', 'Computer vision'],
  install_requires=[
          'scikit-image',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Bio-Informatics ',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  long_description=long_description,
    long_description_content_type='text/markdown'
)
