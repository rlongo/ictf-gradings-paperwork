import os


def verify_file(f):
    '''Check if a file exists'''
    return os.path.exists(f)


def create_file_dirs(f):
    '''Creates parent directories for a given input file'''
    directory = os.path.dirname(f)
    if not os.path.exists(directory):
        os.makedirs(directory)
