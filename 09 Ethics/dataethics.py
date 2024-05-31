# -*- coding: utf-8 -*-
"""DataEthics.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H2R4SDv9CHw0Z2Stb2X4STBbgaAYDOLR
"""

!pip install faker
from faker import Faker
import random
import numpy as np
import pandas as pd

fake = Faker()

# Num employees
num_employees = 10000

# Countries based on 2019 H1B petition percentages
# India: 74.5%, Mainland China: 11.8%, Canada: 1%, South Korea: 0.9%, Philippines: 0.6%, Taiwan: 0.6%, Mexico: 0.6%
# Converted to out of 90 below

india_prob = 74.5 / 90
china_prob = 11.8 / 90
canada_prob = 1 / 90
southkorea_prob = 0.9 / 90
philippines_prob = 0.6 / 90
taiwan_prob = 0.6 / 90
mexico_prob = 0.6 / 90

countries = ['India', 'China', 'Canada', 'South Korea', 'Philippines', 'Taiwan', 'Mexico']
country_distribution = [india_prob, china_prob, canada_prob, southkorea_prob, philippines_prob, taiwan_prob, mexico_prob]
country_origins = np.random.choice(countries, size=num_employees, p=country_distribution)

# Languages
languages = ['Hindi', 'Mandarin', 'French', 'Korean', 'Tagalog', 'Taiwanese', 'Spanish']
language_probs = [india_prob, china_prob, canada_prob, southkorea_prob, philippines_prob, taiwan_prob, mexico_prob]

# Departments
departments = ['Legal', 'Marketing', 'Administrative', 'Operations', 'Sales', 'Finance', 'I/T', 'Product', 'Human Resource']
department_distribution = [0.05, 0.10, 0.10, 0.20, 0.10, 0.05, 0.10, 0.20, 0.10]

department_salaries = {
    'Legal': (40000, 130000),
    'Marketing': (56000, 100000),
    'Administrative': (45000, 70000),
    'Operations': (60000, 120000),
    'Sales': (45000, 80000),
    'Finance': (70000, 130000),
    'I/T': (80000, 120000),
    'Product': (90000, 130000),
    'Human Resource': (50000, 80000)
}

def generate_employee():
    first_name = fake.first_name()
    last_name = fake.last_name()
    ssn = fake.ssn()
    email = fake.email()
    phone = fake.phone_number()
    gender = random.choice(['Male', 'Female'])
    age = random.randint(21, 65)
    job_title = fake.job()
    years_of_experience = random.randint(0, age - 21)
    department = np.random.choice(departments, p=department_distribution)
    salary = random.randint(*department_salaries[department])
    num_langs = np.random.choice([0, 1, 2])
    langs_spoken = random.sample(languages, num_langs)
    country_origin = np.random.choice(countries, p=country_distribution)

    return {
        'First Name': first_name,
        'Last Name': last_name,
        'SSN' : ssn,
        'Email': email,
        'Phone': phone,
        'Gender': gender,
        'Age': age,
        'Job Title': job_title,
        'Years Of Experience': years_of_experience,
        'Salary': salary,
        'Department': department,
        'Languages': ', '.join(langs_spoken),
        'Country of Origin': country_origin
    }

employees = [generate_employee() for _ in range(num_employees)]
employee_df = pd.DataFrame(employees)
employee_df