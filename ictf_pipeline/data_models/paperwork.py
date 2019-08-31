from abc import ABCMeta, abstractmethod

class Paperwork:
    '''Data related to a piece of paperwork'''

    @abstractmethod
    def generate(self, output_file, sub_map):
        """Generates the paperwork from the provided template
        :param output_file: where to save the file
        :param sub_map: dict of str -> values to be used in the sub map
        """
        pass