from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vimba:
        system = vimba.system()

        for feature_name in system.feature_names():
            print(feature_name)
