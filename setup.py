from distutils.core import setup
setup(
  name = 'PyPlaque',        Is
  packages = ['PyPlaque'],
  version = '0.0.1',
  license='GPLv3',
  description = 'Python package for virus plaque analysis based on Plaque2.0',   # Give a short description about your library
  author = 'Plaque2.0 Team, AILS Institute',                   # Type in your name
  author_email = 'ayakimovich@ails.institute',      # Type in your E-Mail
  url = 'https://github.com/plaque2/PyPlaque',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Virus', 'Plaque', 'Virology', 'Microscopy', 'Computer vision'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'scikit-image',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Biologist, bioinformaticians',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GPLv3 License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
