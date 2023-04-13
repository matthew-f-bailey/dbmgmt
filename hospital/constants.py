"""
An underscored attr means that we populate the database with these
for mocking purposes, however these are tables as well, designed to grow.
New ones can be added to the DB as application need arises with no changes here

All others are set and would require code change here to update
"""
GENDER = (('m', 'Male'), ('f', 'Female'))

SPECIALTIES = (
    ("podiatry", "Podiatry"),
    ("general", "General Practice"),
    ("optometry", "Optometry"),
)

NURSE_GRADES = (
    ("a", "A"),
    ("b", "B"),
    ("c", "C"),
)

# SURGICAL
SURGERY_CODES = (
    ("neu", "Neurosurgery"),
    ("pod", "Podiatric Surgery"),
)
SURGERY_CATEGORIES = (
    ("h", "Requires Hospitalization"),
    ("o", "Outpatient"),
)
ANATOMICAL_LOCATIONS = (
    ("foot", "Foot"),
    ("head", "Head")
)
_SURGICAL_SKILLS = (
    ("transplant", "Organ Transplants"), # general
    ("wound", "Wound Care"), # general
    ("brain", "Brain"), # neurosurgery
    ("head_trauma", "Head Trauma"), # neurosurgery
    ("cardiac_arrest", "Cardiac Arrest"), # cardiac_surgery
    ("heart_valve", "Heart Valve Repair"), # cardiac_surgery
    ("rhinoplasty", "Rhinoplasty"), # plastic_surgery
    ("facelift", "Facelift"), # plastic_surgery
)
_SURGICAL_TYPES = (
    ("general_surgery", "General Surgery"),
    ("neurosurgery", "Neurosurgery"),
    ("cardiac_surgery", "Cardiac Surgery"),
    ("plastic_surgery", "Plastic Surgery"),
)

# Medical
BLOOD_TYPE = (
    ("op", "O Positive"),
    ("on", "O Negative"),
)

# Medication interaction severities
MED_INTERACTION = (
    ("s", "Sever Interaction"),
    ("m", "Moderate Interaction"),
    ("l", "Little Interaction"),
)

# Beds, rooms and units
_UNITS = (
    ("gcu", "General Care Unit"),
    ("pou", "Post Operation Unit"),
    ("icu", "Intensive Care Unit"),
    ("brn", "Burn Unit"),
    ("inf", "Infectious Disease Unit"),
)
