import os
import re
import pandas as pd

# Define regular expressions to extract data
name_pattern = r'निर्वाचक का नाम: (.*?)\n'
father_and_husband_name_pattern = r'(?:पिता का नाम:|पति का नाम:) (.*?)\n'
house_number_pattern = r'मकान संख्या (.*?)[\n|: ]'
age_pattern = r'उम्र (\d+) लिंग'
gender_pattern = r'लिंग (.*?)\n'

# Create an empty list to store data from all files
data_list = []

# Specify the folder containing the text files
folder_path = 'output_text'

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
            names = re.findall(name_pattern, data)
            father_and_husband_names = re.findall(father_and_husband_name_pattern, data)
            house_numbers = re.findall(house_number_pattern, data)
            ages = re.findall(age_pattern, data)
            genders = re.findall(gender_pattern, data)
            # Create a list of dictionaries for each file
            file_data = [{'निर्वाचक का नाम': name,
                          'पिता का नाम / पति का नाम': father_and_husband_name,
                          'मकान संख्या': house_number,
                          'उम्र': age,
                          'लिंग': gender}
                         for name, father_and_husband_name, house_number, age, gender in
                         zip(names, father_and_husband_names, house_numbers, ages, genders)]
            data_list.extend(file_data)

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data_list)

# Save the DataFrame to an Excel file
df.to_excel('output.xlsx', index=False)
