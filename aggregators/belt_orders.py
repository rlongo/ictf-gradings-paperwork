from aggregators import Aggregator
from data_models import Student

class BeltOrderAggregator(Aggregator):
    def __init__(self):
        self.vals = dict()

    def process(self, student):
        assert isinstance(student, Student), "record must be a student"

        if not student.belt_level or not student.belt_level.next_level:
            return

        belt_level = student.belt_level.next_level.name
        if belt_level:
            if belt_level not in self.vals:
                self.vals[belt_level] = dict()
            
            size = student.belt_size
            if size not in self.vals[belt_level]:
                self.vals[belt_level][size] = 0

            self.vals[belt_level][size] += 1
    
    def get_header(self):
        return "Belt Level", "Belt Size", "Quantity" 

    def get_stat_iter(self):
        for belt_level, sizes in self.vals.items():
            for size, quantity in sizes.items():
                yield belt_level, size, quantity
        StopIteration()