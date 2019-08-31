#!/bin/python3

import argparse
import os

from parsers import  StudentIteratorExcel, BeltLookupXML, PaperworkJPEGForm, write_aggregator_excel
from data_models import BeltLevel
from aggregators import BeltOrderAggregator, RegistrationListAggregator

from PIL import Image
from fpdf import FPDF

def make_pdf(output_file, pages, dir=''):
    if dir:
        dir += "/"

    cover = Image.open(str(pages[0]))
    width, height = cover.size

    pdf = FPDF(unit="pt", format=[width, height])

    for page in pages:
        pdf.add_page()
        pdf.image(dir + str(page), 0, 0)

    pdf.output(output_file, "F")

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

def pipeline(forms, aggregators, student_iter, output_dir, global_config):
    form_names = set()
    
    # Process the students
    for student in student_iter:
        sub_map = global_config
        sub_map["student"] = student

        for aggregator in aggregators:
            aggregator.process(student)
       
        for dir_name, form_name in student.belt_level.paperwork:
            form = forms[form_name]
            output_file = "{}/{}/{}.{}.jpg".format(output_dir, dir_name, student.fname, student.lname)
            form.generate(output_file, sub_map)
            form_names.add(dir_name)
    
    # Save the aggregators to disk
    for aggregator in aggregators:
        output_file = "{}/GOOD/{}.xlsx".format(output_dir, aggregator.__class__.__name__)
        write_aggregator_excel(output_file, aggregator)

    # Merge the forms into one PDF
    for form_name in form_names:
        filled_forms_dir = os.path.join(output_dir, form_name, )
        target_files = [os.path.join(filled_forms_dir, f) for f in os.listdir(filled_forms_dir)]
        output_file = "{}/GOOD/{}.pdf".format(output_dir, form_name)
        make_pdf(output_file, target_files)

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

    pipeline(forms, aggregators, student_iter, args.output, config)


if __name__== "__main__":
  main()

