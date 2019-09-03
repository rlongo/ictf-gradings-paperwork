from . import Aggregator
from ictf_pipeline.data_models import Student


class RegistrationListAggregator(Aggregator):
    def __init__(self):
        self.students = []

    def process(self, student):
        assert isinstance(student, Student), "record must be a student"
        self.students.append(student)

    def get_header(self):
        return "Name", "Belt Level", "Fee", "Payment Method", "Requires Reciept", "Recieved Belt", "Received Certificate"

    def get_stat_iter(self):
        sorted_list = sorted(self.students,
                             key=lambda student: student.belt_level.name)
        total = 0
        for student in sorted_list:
            yield student.name, student.belt_level.name, student.belt_level.fee, "", "", "", ""
            total += int(student.belt_level.fee)

        yield "TOTAL", "", total, "", "", "", ""

        StopIteration()
