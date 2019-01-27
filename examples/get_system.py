from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vmb:
        system = vmb.system()
        print(system)
