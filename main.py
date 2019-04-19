#!/bin/python3

import argparse
import os

from parsers import  StudentIteratorExcel, BeltLookupXML, PaperworkJPEGForm, write_aggregator_excel
from data_models import BeltLevel
from aggregators import BeltOrderAggregator, RegistrationListAggregator

def get_args():
    parser = argparse.ArgumentParser(description='Throwaway project to generate paperwork required for ictf gradings.')
    parser.add_argument('--students', metavar='students_file', required=True,
                        help='Path to an excel students file')
    parser.add_argument('--forms', metavar='form_dir', required=True,
                    help='Path to a directory with test forms. Test forms must have an xml file, and jpeg.')
    parser.add_argument('--config', metavar='config_file', required=True,
                    help='Path to a config file which has additional params in the format key = value.')
    parser.add_argument('--belts', metavar='belts.xml', required=True,
                    help='Config file for the belts.')
    parser.add_argument('--output', metavar='output dir', required=True,
                    help='Directory where output goes.')
    return parser.parse_args()

def get_config(config_file):
    config = dict()
    with open(config_file) as file:
        for line in file:
            if line.startswith("#"):
                continue # Skip comments
            line = line.split('=')
            if len(line) < 2:
                continue # For empty lines
            config[line[0].strip()] = line[1].strip()
    return config

def main():
    args = get_args()

    forms = dict()
    for file in os.listdir(args.forms):
        if file.endswith(".xml"):
            name = file.split('.')[0]
            form = os.path.join(args.forms, file)

            forms[name] = PaperworkJPEGForm(name, form[:-4], form)

    config = get_config(args.config)
    belt_lookup = BeltLookupXML(args.belts)

    aggregators = [BeltOrderAggregator(), RegistrationListAggregator()]
    
    for student in StudentIteratorExcel(args.students, belt_lookup):
        sub_map = config
        sub_map["student"] = student

        for aggregator in aggregators:
            aggregator.process(student)
        
        for form_name in student.belt_level.paperwork:
            form = forms[form_name]
            output_file = "{}/{}/{}-{}.jpg".format(args.output, form.name, student.fname, student.lname)
            form.generate(output_file, sub_map)
    
    for aggregator in aggregators:
        output_file = "{}/aggregations/{}.xlsx".format(args.output, aggregator.__class__.__name__)
        write_aggregator_excel(output_file, aggregator)


if __name__== "__main__":
  main()