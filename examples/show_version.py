from pymba import Vimba, PYMBA_VERSION


if __name__ == '__main__':
    print('Pymba version: {}'.format(PYMBA_VERSION))
    print('Vimba C API version: {}'.format(Vimba.version()))
