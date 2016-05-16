from setuptools import setup, find_packages
import os, sys, glob, fnmatch

setup(name="pymba",
      version=0.1,
      description="pymba is a Python wrapper for the Allied Vision Technologies (AVT) Vimba C API.",
      long_description="""pymba is a Python wrapper for the Allied Vision Technologies (AVT) Vimba C API. It wraps the VimbaC.dll file included in the AVT Vimba installation to provide a simple Python interface for AVT cameras. It currently supports most of the functionality provided by VimbaC.dll.""",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Manufacturing',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
          'Topic :: Multimedia :: Graphics :: Graphics Conversion',
          'Topic :: Scientific/Engineering :: Image Recognition',
          'Topic :: Software Development :: Libraries :: Python Modules'],
      keywords='python, opencv, cv, machine vision, computer vision, image recognition, vimba, allied vision technologies, avt',
      author='morefigs',
      author_email='morefigs@gmail.com',
      url='https://github.com/morefigs/pymba',
      license='BSD',
      packages=['pymba', 'pymba.tests'],
      zip_safe=False,
      requires=['numpy'],
)
