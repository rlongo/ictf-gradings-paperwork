#!/bin/python3

import os

from ictf_pipeline.parsers import  StudentIteratorExcel, BeltLookupXML, PaperworkJPEGForm, write_aggregator_excel
from ictf_pipeline.data_models import BeltLevel
from ictf_pipeline.aggregators import BeltOrderAggregator, RegistrationListAggregator

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

def ictf_pipeline(forms, aggregators, student_iter, output_dir, global_config):
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
