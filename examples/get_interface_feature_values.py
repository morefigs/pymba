from pymba import Vimba, VimbaException


if __name__ == '__main__':

    with Vimba() as vmb:
        interface = vmb.interface(0)
        interface.open()

        # get feature value via feature object
        for feature_name in interface.feature_names():
            feature = interface.feature(feature_name)

            try:
                value = feature.value

                # alternatively the feature value can be read as an object attribute
                # value = getattr(interface, feature_name)
                # or
                # value = interface.someFeatureName

            except VimbaException as e:
                value = e

            print(feature_name, '--', value)

        interface.close()
