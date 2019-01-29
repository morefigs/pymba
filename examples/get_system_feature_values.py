from pymba import Vimba, VimbaException


if __name__ == '__main__':

    with Vimba() as vimba:
        system = vimba.system()

        # get feature value via feature object
        for feature_name in system.feature_names():
            feature = system.feature(feature_name)

            try:
                value = feature.value

                # alternatively the feature value can be read as an object attribute
                # value = getattr(system, feature_name)
                # or
                # value = system.someFeatureName

            except VimbaException as e:
                value = e

            print(feature_name, '--', value)
