from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()
        camera.load_config(b'sample_config.xml')
        camera.close()
