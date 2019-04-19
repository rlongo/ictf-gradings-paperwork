from abc import ABCMeta, abstractmethod

class BeltLevel:
    '''Information pertaining to the current belt level'''
    
    def __init__(self, name, match_pattern, next_level, attributes):
        """Constructs a new belt level record
        :param name: Human name for this belt level
        :param match_pattern: Regex to test possible inputs against to verify
            that a given input is this belt level
        :param next_level: The next BeltLevel. Can be nil
        :param attributes: List of attributes specific to the given belt level
        """
        self.name = name
        self.match_pattern = match_pattern
        self.next_level = next_level
        self.attributes = attributes
    
    def __str__(self):
        next_level = "None"
        if self.next_level:
            next_level = self.next_level.name
        return "Belt Level: {} (Next: {}), {}".format(self.name, next_level, str(self.attributes))


class Student:
    '''Information about a single student'''
    
    def __init__(self, fname, lname, belt_level, belt_size):
        self.fname = fname
        self.lname = lname
        self.belt_level = belt_level
        self.belt_size = belt_size
    
    def __str__(self):
        return "Student: {} {}, {}, Size {}".format(self.fname, self.lname, self.belt_level.name, self.belt_size)


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

