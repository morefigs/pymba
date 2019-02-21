from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        # read a feature value
        feature = camera.feature('ExposureAuto')
        value = feature.value

        # set the feature value
        feature.value = value

        print(feature.name, '=', feature.value)

        # alternatively the feature value can be set as an object attribute
        camera.ExposureAuto = feature.value

        camera.close()
