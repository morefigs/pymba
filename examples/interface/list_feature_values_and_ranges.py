from pymba import Vimba, VimbaException


if __name__ == '__main__':

    with Vimba() as vimba:
        interface = vimba.interface(0)
        interface.open()

        # get feature value via feature object
        for feature_name in interface.feature_names():
            feature = interface.feature(feature_name)
            try:
                value = feature.value
                range_ = feature.range

                # alternatively the feature value can be read as an object attribute
                # value = getattr(interface, feature_name)
                # or
                # value = interface.someFeatureName

            except VimbaException as e:
                value = e
                range_ = None

            print('\n\t'.join(
                str(x) for x in (
                    feature_name,
                    f'value: {value}',
                    f'range: {range_}')
                if x is not None))

        interface.close()
