import pandas as pd
import re

from student_iterator import StudentIterator, Student

class StudentIteratorExcel(StudentIterator):
    def __init__(self, file, belt_levels):
        self.belt_levels = belt_levels
        self.df = pd.ExcelFile(file).parse(0)
        self.rowiter = self.df.iterrows()

    def next(self):
        row = next(self.rowiter)[1]
        level = self.get_belt_level(row["Belt Level"])
        return  Student(row["First Name"], row["Last Name"], level, row["Belt Size"])

    def get_belt_level(self, claimed_belt_level):
        """Attempts to get the given belt level for a claimed belt level
        :param claimed_belt_level: What the claim is
        """

        for level in self.belt_levels:
            if re.compile(level.match_pattern).match(claimed_belt_level.lower()):
                return level
        
        raise RuntimeError("Failed to parse belt level '{}'".format(claimed_belt_level))

