from pymba import Vimba, __version__


if __name__ == '__main__':
    print('Pymba version: {}'.format(__version__))
    print('Vimba C API version: {}'.format(Vimba.version()))
