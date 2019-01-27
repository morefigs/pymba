from pymba import Vimba, VimbaException


if __name__ == '__main__':

    with Vimba() as vmb:
        print(vmb.interface_ids())
