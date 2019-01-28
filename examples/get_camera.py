from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vmb:
        # provide camera index or id
        camera = vmb.camera(0)
        print(camera)
