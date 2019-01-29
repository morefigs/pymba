from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vimba:
        # provide interface index or id
        interface = vimba.interface(0)
        print(interface)
