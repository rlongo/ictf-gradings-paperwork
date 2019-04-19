import pandas as pd
import re

from data_models import StudentIterator, Student

class StudentIteratorExcel(StudentIterator):
    def __init__(self, file, belt_lookup):
        self.belt_lookup = belt_lookup
        self.df = pd.ExcelFile(file).parse(0)
        self.rowiter = self.df.iterrows()

    def next(self):
        row = next(self.rowiter)[1]
        level = self.belt_lookup.get_belt_level(row["Belt Level"])
        return  Student(row["First Name"], row["Last Name"], level, row["Belt Size"])
        