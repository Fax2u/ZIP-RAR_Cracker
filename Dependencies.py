import os


def install_library(library_name):
    try:
        print(f'Installing {library_name} Library')
        os.system(f'pip install {library_name}')
    except Exception as e:
        print(f'Error installing {library_name}: {e}')


if __name__ == '__main__':
    library_list = ['zipp', 'patool', 'rarfile', 'multiprocessing']
    for lib in library_list:
        install_library(lib)

