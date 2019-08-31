# ICTF Gradings Paperwork
A project to generate paperwork required for ictf gradings.

## Architecture

The project is designed as a pipeline with several map-reduce steps:
1. Input of:
    1. Student Information
    2. Belt Levels & Form Templates
    3. Other Inputs to render on forms
2. MAP `aggregator`: matches student info to belt info

From there, the output of `StudentIterator` can be fed into multiuple different
map or reduce methods (`PaperworkGenerator`) which consume that output and
produce some form of paperwork.

## Inputs

```
 python3 main.py --students inputs/students.xlsx --forms inputs/forms/ --config inputs/config --belts inputs/belts.xml --output=outputs/
```
| INPUT |  |
|---|---|
| students | students EXCEL file. Header must be `First Name, Last Name, Belt Size, Belt Level` |
| forms | List of forms to fill out. Currently a form is a jpg image that has a matching `name.jpeg.xml` which defines how to fill it in. Example below |
| config | `key = value`. Used as substititions in forms |
| belts | xml specifying data about each belt level. Example below |
| output | where does the output go |

### students example

```
First Name  Last Name  Belt Size  Belt Level
Rob         Dylan      size 5	  blue 
Ari         Sikar      size 000   little dragon white
Jamie       Smith      3          little dragon orange stripe
Lily        Ha         7          black stripe
Ming        Po         2          red stripe
```

### forms example

Assumes you have a jpeg to dump text ontop of.
```xml
<?xml version="1.0"?>
<template>
    <field name="student.lname" x="90" y="180" font="Roboto-Regular.ttf" font_colour="#2196f3" font_size="18"></field>
    <field name="student.fname" x="500" y="180" font="Roboto-Regular.ttf" font_colour="#2196f3" font_size="18"></field>
    <field name="student.belt_level.name" x="127" y="430" font="Roboto-Regular.ttf" font_colour="#2196f3" font_size="18"></field>
    <field name="head_instructor" x="525" y="270" font="Roboto-Regular.ttf" font_colour="#2196f3" font_size="18"></field>
    <field name="dojang" x="125" y="270" font="Roboto-Regular.ttf" font_colour="#2196f3" font_size="18"></field>
</template>
```

### belts example

Example of belts input. Note that:
* match_pattern is a regex
* next_belt can be omitted
* attributes is a dictionary of values that paperwork can pull in

```xml
<?xml version="1.0"?>
<belts>
    <belt id="1" name="Little Dragon White Belt" next_belt="2">
        <match_pattern>little\s?dragon\s+white\s*(?:belt)?</match_pattern>

        <paperworks>
            <paperwork>LD_White_to_Orange_stripe</paperwork>
            <paperwork>certificate</paperwork>
        </paperworks>

        <attributes>
            <attribute name="fee">35</attribute>
        </attributes>
    </belt>
</belts>
```

### config example

```ini
head_instructor = Mr. T. Taekwondo
dojang = NTCC
date_year = 2019
date_month = Aug
date_day = 14
```

## Paperwork Generators

### 1. Test Form
Generates test forms for each student.

### 2. Certificate Generator
Generates certificates for each student.

### 3. Belt Orders
Creates a master list of belt orders to be placed.

### 4. Master List
Master list of students going for test (used for tracking payments and whatnot).



