# Pymba

Pymba is a Python wrapper for Allied Vision's Vimba C API. It wraps the Vimba C library file included in the Vimba installation to provide a simple Python interface for Allied Vision cameras. It currently supports most of the functionality provided by Vimba.

## Installation

### Installing Vimba SDK

For Windows:
* [Download](https://www.alliedvision.com/en/products/software.html) and launch the Vimba SDK installer:
  * Select "Custom Selection".
  * Select (at least) the following options:
    * A transport layer that matches your hardware (e.g. "Vimba USB Transport Layer" for USB cameras):
      * Core components.
      * Register GenICam Path variable.
    * Vimba SDK:
      * Core components.
      * Register environment variables.
      * C API runtime components.
      * C API development components.
      * Driver Installer.
      * Vimba Viewer.
* Run `VimbaDriverInstaller.exe` and install the relevant driver.
* Test the driver installation by running `VimbaViewer.exe`.

For other OS's see [Vimba's download page](https://www.alliedvision.com/en/products/software.html).

### Installing Pymba

For Python 3 install Pymba via PIP.

    pip install pymba
    
For Python 2 and for backwards compatibility with older versions of Pymba use the [`python2`](https://github.com/morefigs/pymba/tree/python2) branch.

### Testing installation 

If Vimba and Pymba are installed correctly, then the following code should give the installed Vimba version. No camera is needed.

    from pymba import Vimba, PYMBA_VERSION
    
    print(PYMBA_VERSION)
    print(Vimba.version())
    
## Usage examples
    
Usage examples can be found in the [`examples`](examples/) directory.

## Known issues

* Not all API functions are supported, but missing functions can be added on request.
* Not all camera pixel formats are currently supported.
