class Paperwork:
    '''Data related to a piece of paperwork'''

    def __init__(self, file_path, sub_map):
        """Constructs a new piece of paperwork
        :param file_path: path to the file
        :param sub_map: dict of value to place into an x,y coordinate
        """
        self.file_path = file_path
        self.sub_map = sub_map

