from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vimba:
        interface = vimba.interface(0)
        interface.open()

        # set a feature value by feature name
        feature = interface.feature('InterfacePingPace')
        print(feature.value)
        feature.value = 3
        print(feature.value)

        # alternatively the feature value can be set as an object attribute
        interface.InterfacePingPace = 3

        interface.close()
