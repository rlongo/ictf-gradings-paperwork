from abc import ABCMeta, abstractmethod
import re

class BeltLevel:
    '''Information pertaining to the current belt level'''
    
    def __init__(self, name, match_pattern, next_level, paperwork, attributes):
        """Constructs a new belt level record
        :param name: Human name for this belt level
        :param match_pattern: Regex to test possible inputs against to verify
            that a given input is this belt level
        :param next_level: The next BeltLevel. Can be nil
        :param papaerwork: Paperwork relevant to this belt level
        :param attributes: List of attributes specific to the given belt level
        """
        self.name = name
        self.match_pattern = match_pattern
        self.next_level = next_level
        self.paperwork = paperwork
        self.attributes = attributes
    
    def __str__(self):
        next_level = "None"
        if self.next_level:
            next_level = self.next_level.name
        return "Belt Level: {} (Next: {}), {}".format(self.name, next_level, str(self.attributes))


class BeltLookup:
    '''Interface to get belt info'''

    def get_belt_level(self, claimed_belt_level):
        """Gets belt level matchine the input against the belt's match pattern
        :param claimed_belt_level: string to match against the input regex
        """
        belt_levels = self._get_belt_levels()

        for level in belt_levels:
            if re.compile(level.match_pattern).match(claimed_belt_level.lower()):
                return level
        
        raise RuntimeError("Failed to parse belt level '{}'".format(claimed_belt_level))

    @abstractmethod
    def _get_belt_levels(self):
        """Gets belt levels we currently support
        """
        pass
