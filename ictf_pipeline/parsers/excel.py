import pandas as pd
import re
import xlsxwriter

from ictf_pipeline.data_models import StudentIterator, Student
from ictf_pipeline.aggregators import Aggregator
import ictf_pipeline.parsers.helpers as helpers

class StudentIteratorExcel(StudentIterator):
    def __init__(self, file, belt_lookup):
        self.belt_lookup = belt_lookup
        self.df = pd.ExcelFile(file).parse(0)
        self.rowiter = self.df.iterrows()

    def next(self):
        row = next(self.rowiter)[1]
        level = self.belt_lookup.get_belt_level(row["Belt Level"])
        size = self._sanitize_belt_size(row["Belt Size"])
        return  Student(row["First Name"], row["Last Name"], level, size)
    
    def _sanitize_belt_size(self, size):
        '''Reformats belt size string as 'Size 00' '''
        regex = r"(?:size)?\s*(\d+)"
        matches = re.finditer(regex, str(size).lower(), re.MULTILINE)
        input_size = next(matches).groups()[0]
        return "Size {}".format(input_size)


def write_aggregator_excel(output_file, aggregator):
    """Writes out an aggregator to excel
    :param output_file: The file to save data to
    :param aggregator: Where to read data from
    """
    assert isinstance(aggregator, Aggregator), "Must provide an aggregator"

    helpers.create_file_dirs(output_file)

    df = pd.DataFrame(columns=list(aggregator.get_header()))
    for i, row in enumerate(aggregator):
        df.loc[i] = list(row)

    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save() 