from pymba.vimba import Vimba


if __name__ == '__main__':

    with Vimba() as vmb:
        print(vmb.get_interface_ids())
