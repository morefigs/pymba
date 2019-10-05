from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()
        camera.load_config(b'gabri.xml')
        for feature_name in camera.feature_names():
            feature = camera.feature(feature_name)
            print(feature.info)

        camera.close()
