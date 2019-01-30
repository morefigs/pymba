# Pymba

Pymba is a Python wrapper for Allied Vision's Vimba C API. It wraps the VimbaC library file included in the Vimba installation to provide a simple Python interface for Allied Vision cameras. It currently supports most of the functionality provided by Vimba.

## Requirements

### Vimba SDK

* Download and run the Vimba SDK installer from Allied Vision from https://www.alliedvision.com/en/products/software.html.
* Select "Custom Selection".
* Select (at least) the following options:
  * A transport layer that matches your hardware (e.g. "Vimba USB Transport Layer" for USB cameras)
    * Core components
    * Register GenICam Path variable
  * Vimba SDK
    * Core components
    * Register environment variables
    * C API runtime components
    * C API development components
    * Driver Installer
    * Vimba Viewer
* Run `VimbaDriverInstaller.exe` and install the relevant driver.
* Test the driver installation by running `VimbaViewer.exe`.

## Installation

Install Pymba via PIP.

    pip install pymba

## Testing installation 

If Vimba and pymba are installed correctly, then the following code examples should give the installed Vimba version. No camera is needed.

    from pymba import Vimba
    
    print(Vimba.version())
    
## Usage examples
    
Usage examples can be found in [examples/](examples/).

## Known issues

* Not all API functions are supported.
* Not all camera pixel formats are currently supported.

