from setuptools import setup
from pymba import __version__


setup(name='pymba',
      version=__version__,
      description="Pymba is a Python wrapper for Allied Vision's Vimba C API.",
      long_description=(
          "Pymba is a Python wrapper for Allied Vision's Vimba C API. It wraps the Vimba C library "
          "file included in the Vimba installation to provide a simple Python interface for Allied "
          "Vision cameras. It currently supports most of the functionality provided by Vimba."
      ),
      # https://pypi.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Healthcare Industry',
          'Intended Audience :: Manufacturing',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
          'Topic :: Multimedia :: Video :: Capture',
          'Topic :: Scientific/Engineering :: Image Recognition',
          'Topic :: Scientific/Engineering :: Visualization',
      ],
      keywords='python, python3, opencv, cv, machine vision, computer vision, image recognition, vimba, allied vision',
      author='morefigs',
      author_email='morefigs@gmail.com',
      url='https://github.com/morefigs/pymba',
      license='MIT',
      packages=[
          'pymba',
      ],
      zip_safe=False,
      install_requires=[
          'numpy',
      ],
      extras_requires={
          'dev': [
              'opencv-python',
              'pytest',
          ]
      }
      )

# python3 -m pip install --user --upgrade setuptools wheel twine
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload dist/*
