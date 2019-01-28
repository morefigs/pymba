from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vmb:
        camera = vmb.camera(0)
        camera.open()

        for feature_name in camera.feature_names():
            feature = camera.feature(feature_name)
            print(feature.info)

        camera.close()
