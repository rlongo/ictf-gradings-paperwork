#!/bin/python3

import argparse
import os

from student_iterator import  StudentIteratorExcel, BeltLevel
from paperwork import TemplateForm

def get_belt_levels():
    belts = [BeltLevel("Little Dragon White Belt", r"little\s?dragon\s+white\s*(?:belt)?", None, {"fee":  35}),
                BeltLevel("Little Dragon Orange Stripe", r"little\s?dragon\s+(orange\s*(?:stripe)?)\s*(?:belt)?", None, {"fee":  40}),
                BeltLevel("Little Dragon Green Stripe", r"little\s?dragon\s+(green\s*(?:stripe)?)\s*(?:belt)?", None, {"fee":  45}),
                BeltLevel("Little Dragon Blue Stripe", r"little\s?dragon\s+(blue\s*(?:stripe)?)\s*(?:belt)?", None, {"fee":  50}),
                BeltLevel("Little Dragon Red Stripe", r"little\s?dragon\s+(red\s*(?:stripe)?)\s*(?:belt)?", None, {"fee":  55}),
                BeltLevel("Little Dragon Grey", r"little\s?dragon\s+(grey\s*(?:stripe)?)\s*(?:belt)?", None, {"fee":  60}),
                BeltLevel("White", r"white\s*stripe\s*(?:belt)?", None, {"fee":  70}),
                BeltLevel("Yellow Stripe", r"yellow\s*stripe\s*(?:belt)?", None, {"fee":  80}),
                BeltLevel("Yellow", r"yellow\s*(?:belt)?", None, {"fee":  90}),
                BeltLevel("Green Stripe", r"green\s*stripe\s*(?:belt)?", None, {"fee":  100}),
                BeltLevel("Green", r"green\s*(?:belt)?", None, {"fee":  110}),
                BeltLevel("Blue Stripe", r"blue\s*stripe\s*(?:belt)?", None, {"fee":  125}),
                BeltLevel("Blue", r"blue\s*(?:belt)?", None, {"fee":  145}),
                BeltLevel("Red Stripe", r"red\s*stripe\s*(?:belt)?", None, {"fee":  165}),
                BeltLevel("Red", r"red\s*(?:belt)?", None, {"fee":  205}),
                BeltLevel("Black Stripe", r"black\s*stripe\s*(?:belt)?", None,  {"fee":  550}),
                BeltLevel("Black Belt Level Tests", r"black\s*belt.*", None, {"fee":  50})]

    for i in range(len(belts)-2):
        belts[i].next_level = belts[i+1]
    return belts 

def get_args():
    parser = argparse.ArgumentParser(description='Throwaway project to generate paperwork required for ictf gradings.')
    parser.add_argument('--students', metavar='students_file', required=True,
                        help='Path to an excel students file')
    parser.add_argument('--forms', metavar='form_dir', required=True,
                    help='Path to a directory with test forms. Test forms must have an xml file, and jpeg.')
    parser.add_argument('--config', metavar='config_file', required=True,
                    help='Path to a config file which has additional params in the format key = value.')
    parser.add_argument('--output', metavar='output dir', required=True,
                    help='Directory where output goes.')
    return parser.parse_args()

def get_config(config_file):
    config = dict()
    with open(config_file) as file:
        for line in file:
            line = line.split('=')
            config[line[0].strip()] = line[1].strip()
    return config

def main():
    args = get_args()

    forms = []
    for file in os.listdir(args.forms):
        if file.endswith(".xml"):
            name = file.split('.')[0]
            form = os.path.join(args.forms, file)

            forms.append(TemplateForm(name, form[:-4], form))

    config = get_config(args.config)

    for student in StudentIteratorExcel(args.students, get_belt_levels()):
        sub_map = config
        sub_map["student"] = student

        for form in forms:
            form.generate("{}/{}/{}-{}.testform.jpg".format(args.output, form.name, student.fname, student.lname), sub_map)
  
if __name__== "__main__":
  main()