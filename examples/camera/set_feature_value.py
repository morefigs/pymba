from pymba import Vimba


FEATURE_NAME = 'PixelFormat'


if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        # read a feature value
        feature = camera.feature(FEATURE_NAME)
        value = feature.value

        # set the feature value (with the same value)
        feature.value = value

        print('"{}" was set to "{}"'.format(feature.name, feature.value))

        camera.close()
