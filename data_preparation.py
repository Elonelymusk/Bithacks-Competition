# Imports
import csv
import pandas as pd

# Convert dataset to dataframe
dataframe = pd.read_csv("symptoms_illness_dataset.csv")

# 1st pass at cleaning the dataset -- put it in the right format
current_illness = "Fungal infection"
illness_list = []
symptom_list = []
for row in dataframe.iterrows():
    # Illness   ->  row[1][0]
    # Symptom 1 ->  row[1][1]
    # Symptom x ->  row[1][x]

    # Extract all symptoms
    illness = row[1][0]
    if illness == current_illness:
        for symptom in row[1][1:]:
            if str(symptom) != 'nan':
                if str(symptom) not in symptom_list:
                    symptom_list.append(str(symptom))
    else:
        symptom_list.insert(0, current_illness)
        illness_list.append(symptom_list)
        symptom_list = []
        current_illness = illness

# 2nd pass at cleaning the dataset -- find first duplicate, cut after that
check_string = "Fungal infection"

for index in range(len(illness_list[2:])):
    if illness_list[index][0] == check_string and index > 0:
        illness_list = illness_list[:index]
        break

# Equalize the length of the lists


# Make a dictionary out of the remaining list
illness_dict = {}
for element in illness_list:
    illness_dict[element[0]] = element[1:]

# `illness_dict` compares each disease to their symptoms
print(illness_dict)
