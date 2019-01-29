from pymba import Vimba, VimbaException


if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        # get feature value via feature object
        for feature_name in camera.feature_names():
            feature = camera.feature(feature_name)

            try:
                value = feature.value

                # alternatively the feature value can be read as an object attribute
                # value = getattr(camera, feature_name)
                # or
                # value = camera.someFeatureName

            except VimbaException as e:
                value = e

            print(feature_name, '--', value)

        camera.close()
