from pymba import Vimba, PYMBA_VERSION


if __name__ == '__main__':
    print(f'Pymba version: {PYMBA_VERSION}')

    vmb = Vimba()
    print(f'Vimba version: {vmb.version}')
