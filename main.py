#!/bin/python3

import argparse

from student_iterator import  StudentIteratorExcel, BeltLevel

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

def main():
    parser = argparse.ArgumentParser(description='Throwaway project to generate paperwork required for ictf gradings.')
    parser.add_argument('--students', metavar='students_file', required=True,
                        help='the path to an excel students file')
    args = parser.parse_args()

    for student in StudentIteratorExcel(args.students, get_belt_levels()):
        print(student)
  
if __name__== "__main__":
  main()