from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vmb:
        system = vmb.system()
        for feature_name in system.feature_names():
            print(feature_name)
