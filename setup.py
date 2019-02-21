from setuptools import setup

from pymba import PYMBA_VERSION


setup(name='pymba',
      version=PYMBA_VERSION,
      description="Pymba is a Python wrapper for Allied Vision's Vimba C API.",
      long_description="Pymba is a Python wrapper for Allied Vision's Vimba C API. It wraps the Vimba C library file "
                       "included in the Vimba installation to provide a simple Python interface for Allied Vision "
                       "cameras. It currently supports most of the functionality provided by Vimba.",
      # https://pypi.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Healthcare Industry',
          'Intended Audience :: Manufacturing',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
          'Topic :: Multimedia :: Video :: Capture',
          'Topic :: Scientific/Engineering :: Image Recognition',
          'Topic :: Scientific/Engineering :: Visualization',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      keywords='python, python3, opencv, cv, machine vision, computer vision, image recognition, vimba, allied vision',
      author='morefigs',
      author_email='morefigs@gmail.com',
      url='https://github.com/morefigs/pymba',
      license='GPL-3.0',
      packages=[
          'pymba',
      ],
      zip_safe=False,
      install_requires=[
          'numpy',
      ],
      extras_requires={
          'dev': [
              'pytest',
          ]
      }
      )

# python3 -m pip install --user --upgrade setuptools wheel twine
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload dist/*
