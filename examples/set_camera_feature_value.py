from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vmb:
        camera = vmb.camera(0)
        camera.open()

        # set a feature value by feature name
        feature = camera.feature('ExposureAuto')
        print(feature.value)
        feature.value = feature.value

        # alternatively the feature value can be set as an object attribute
        camera.ExposureAuto = feature.value

        camera.close()
