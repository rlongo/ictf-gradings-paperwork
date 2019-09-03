from abc import ABCMeta, abstractmethod


class Aggregator:

    @abstractmethod
    def process(self, student):
        '''processes the given record'''
        pass

    @abstractmethod
    def get_header(self):
        '''Returns a tuple of strings which can be used as the stats header'''
        pass

    def __iter__(self):
        self.iter = self.get_stat_iter()
        return self

    def __next__(self):
        """Iterator for stats rows"""
        return next(self.iter)

    @abstractmethod
    def get_stat_iter(self):
        pass
