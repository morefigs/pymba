from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vimba:
        # provide camera index or id
        camera = vimba.camera(0)
        print(camera)
