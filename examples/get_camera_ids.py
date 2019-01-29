from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vimba:
        print(vimba.camera_ids())
