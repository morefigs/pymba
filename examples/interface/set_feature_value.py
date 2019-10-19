from pymba import Vimba


FEATURE_NAME = 'InterfacePingPace'


if __name__ == '__main__':

    with Vimba() as vimba:
        interface = vimba.interface(0)
        interface.open()

        # read a feature value
        feature = interface.feature(FEATURE_NAME)
        value = feature.value

        # set the feature value (with the same value)
        feature.value = value

        print('"{}" was set to "{}"'.format(feature.name, feature.value))

        interface.close()
