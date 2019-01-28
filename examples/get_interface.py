from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vmb:
        # provide interface index or id
        interface = vmb.interface(0)
        print(interface)
