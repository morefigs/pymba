from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vimba:
        system = vimba.system()
        print(system)
