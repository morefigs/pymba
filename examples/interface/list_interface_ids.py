from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vimba:
        print(vimba.interface_ids())
