# ICTF Gradings Paperwork
Throwaway project to generate paperwork required for ictf gradings.

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

## Paperwork Generators

### 1. Test Form
Generates test forms for each student.

### 2. Certificate Generator
Generates certificates for each student.

### 3. Belt Orders
Creates a master list of belt orders to be placed.

### 4. Master List
Master list of students going for test (used for tracking payments and whatnot).



