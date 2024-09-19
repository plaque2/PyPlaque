import pathlib

from setuptools import setup, find_packages

import PyPlaque

# read the contents of your README file



cwd = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (cwd / 'README.md').read_text(encoding='utf-8')

version = 'v0.2.1'

setup(
  name = 'PyPlaque',
  packages=find_packages(include=['PyPlaque', 'PyPlaque.*']),
  version = version,
  license='GPLv3',
  description = 'Python package for virus plaque analysis based on Plaque2.0',
  author = 'Plaque2.0 Team, AILS Institute, CASUS HZDR',
  author_email = 'ayakimovich@ails.institute',
  url = 'https://github.com/plaque2/PyPlaque',
  download_url = 'https://github.com/plaque2/PyPlaque/archive/{}.tar.gz' \
            .format(version),
  keywords = ['Virus', 'Plaque', 'Virology', 'Microscopy', 'Computer vision'],
  python_requires=">=3.9, <=3.12",
  install_requires=[
          'scikit-image>=0.24.0',
          'numpy>=2.0.0',
          'matplotlib>=3.7.0',
          'opencv-python>=4.10.0.84',
          'Pillow>=10.3.0',
          'pandas>=1.5.3',
          'scipy>=1.13.1',
          'scikit-learn>=1.5.0',
          'seaborn==0.12.2',
          'tqdm>=4.66.4',
          'tifffile>=2023.2.28'
      ],
  extras_require={
          'test': ['pytest>=8.1.1']
      },
  classifiers=[
     'Development Status :: 3 - Alpha',
     'Intended Audience :: Science/Research',
     'Topic :: Scientific/Engineering :: Bio-Informatics ',
     'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
     'Programming Language :: Python :: 3.9',
     'Programming Language :: Python :: 3.10',
     'Programming Language :: Python :: 3.11',
     'Programming Language :: Python :: 3.12'
      ],

  long_description=long_description,
  long_description_content_type='text/markdown'
)
