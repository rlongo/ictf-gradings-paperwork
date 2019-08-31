#!/bin/python3

import argparse
import os

from ictf_pipeline.parsers import  StudentIteratorExcel, BeltLookupXML, PaperworkJPEGForm
from ictf_pipeline.aggregators import BeltOrderAggregator, RegistrationListAggregator
from ictf_pipeline import ictfpl

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

    aggregators = [BeltOrderAggregator(), RegistrationListAggregator()]

    forms = dict()

    config = get_config(args.config)
    belt_lookup = BeltLookupXML(args.belts)

    # Get all forms
    for file in os.listdir(args.forms):
        if file.endswith(".xml"):
            name = file.split('.')[0]
            form = os.path.join(args.forms, file)
            forms[name] = PaperworkJPEGForm(name, form[:-4], form)

    student_iter = StudentIteratorExcel(args.students, belt_lookup)

    ictfpl(forms, aggregators, student_iter, args.output, config)


if __name__== "__main__":
  main()

