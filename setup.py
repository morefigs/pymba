from setuptools import setup


setup(name='pymba',
      version=0.1,
      description="Pymba is a Python wrapper for Allied Vision's Vimba SDK.",
      long_description="Pymba is a Python wrapper for Allied Vision's Vimba SDK. It uses the Vimba C API included in "
                       "the Allied Vision Vimba installation to provide a simple Python interface for Allied Vimba "
                       "cameras.",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Manufacturing',
          'License :: OSI Approved :: GPL-3.0 License',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
          'Topic :: Multimedia :: Graphics :: Graphics Conversion',
          'Topic :: Scientific/Engineering :: Image Recognition',
          'Topic :: Software Development :: Libraries :: Python Modules'],
      keywords='python, opencv, machine vision, computer vision, image recognition, vimba, vimba-sdk, allied vision',
      author='morefigs',
      author_email='morefigs@gmail.com',
      url='https://github.com/morefigs/pymba',
      license='GPL-3.0',
      packages=['pymba'],
      zip_safe=False,
      requires=['numpy'])
