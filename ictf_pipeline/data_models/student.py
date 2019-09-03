from abc import ABCMeta, abstractmethod


class Student:
    '''Information about a single student'''

    def __init__(self, fname, lname, belt_level, belt_size):
        self.fname = fname
        self.lname = lname
        self.name = "{} {}".format(fname, lname)
        self.belt_level = belt_level
        self.belt_size = belt_size

    def __str__(self):
        return "Student: {} {}, {}, Size {}".format(
            self.fname, self.lname, self.belt_level.name, self.belt_size)


class StudentIterator:
    '''Interface to some form of iterator that produces students'''

    def __iter__(self):
        return self

    def __next__(self):
        """Iterator for students
        :return Student or iteration stops
        """
        return self.next()

    @abstractmethod
    def next(self):
        pass
