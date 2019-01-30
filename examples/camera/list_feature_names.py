from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        for feature_name in camera.feature_names():
            print(feature_name)

        camera.close()
