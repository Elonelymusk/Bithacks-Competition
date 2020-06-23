# Imports
import csv
import pandas as pd
import json

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

# Make a list of all of the symptoms -- this will be used later
symptom_list = []
for element in illness_list:
    symptoms = element[1:]
    for symptom in symptoms:
        symptom_list.append(symptom)
# Remove duplicates (I don't know how it works, it just does)
symptoms = list(dict.fromkeys(symptom_list))

# Find the element of greatest length in the array
greatest = 0
for element in illness_list:
    length = len(element)
    if length > greatest:
        greatest = length

# Equalize the length of the lists
for element in illness_list:
    length = len(element)
    difference = greatest - length
    for cycle in range(difference):
        element.append("None")

# Make a dictionary out of the remaining list
illness_dict = {}
for element in illness_list:
    illness_dict[element[0]] = element[1:]

# `illness_dict` compares each disease to their symptoms
illness_dataframe = pd.DataFrame(data=illness_dict)
#print(illness_dataframe)

#########################################
# At this point, the dataset is ready.  #
# Now to make the intents.json file.    #
#########################################

json_data = {}

for symptom in symptoms:
    json_data[symptom] = {}

# Wrap the data in the "intents" tag
json_data = {"intents": [json_data]} 

print(json_data)
with open('intents.json', 'w') as outfile:
    json.dump(json_data, outfile)