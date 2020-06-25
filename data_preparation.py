# Imports
import csv
import pandas as pd
import json

def process_dataset():
    # Convert dataset to dataframe
    dataframe = pd.read_csv("symptoms_illness_dataset.csv")

    # 1st pass at cleaning the dataset -- put it in the right format
    current_illness = "Fungal infection"
    illness_list = []
    symptom_list = []
    for row in dataframe.iterrows():
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

    # Reduce number of illnesses based on the blacklist
    blacklist = []
    with open("illness_blacklist.csv", newline='') as file:
        reader = csv.reader(file)
        blacklist = list(reader)[0]
    for element in blacklist:
        for item in illness_list:
            if item[0] == element:
                illness_list.remove(item)

    # Make a list of all of the symptoms -- this will be used later
    symptom_list = []
    for element in illness_list:
        symptoms = element[1:]
        for symptom in symptoms:
            symptom_list.append(symptom)
    # Remove duplicates (I don't know how it works, it just does)
    symptoms = list(dict.fromkeys(symptom_list))
    #print(symptoms)

    # Push all symptoms to a few files --- TEMP- THIS WILL BE REMOVED
    #temp_symptoms = symptoms
    #break_list = [24, 23, 23, 23]
    #for i in range(4):
    #    with open(f"symptoms{i}.txt", "w") as symptom_file:
    #        try:
    #            for j in range(int(break_list[i])-1):
    #                symptom_file.write(str(temp_symptoms[j]).strip() + "\n")
    #                del temp_symptoms[j]
    #        except IndexError:
    #            pass
    #    symptom_file.close()

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
        for _cycle in range(difference):
            element.append("None")

    # Make a dictionary out of the remaining list
    illness_dict = {}
    for element in illness_list:
        illness_dict[element[0]] = element[1:]

    # `illness_dict` compares each disease to their symptoms
    illness_dataframe = pd.DataFrame(data=illness_dict)
    illness_dataframe.to_csv('dataset.csv', index=False)

    #########################################
    # At this point, the dataset is ready.  #
    # Now to make the intents.json file.    #
    #########################################

    # Automate the responses for each symptom <---- Easy
    def form_response(symptom):
        first_response = f"Ok, I've detected '{symptom}', anything else?"
        second_response = f"Alright, it looks like you have '{symptom}', are you experiencing any other symptoms?"
        third_response = f"So, it seems like you have '{symptom}', any other symptoms?"

        return [first_response,  second_response, third_response]

    # Automate the patterns for each symtom <---- HARD
    def form_pattern(symptom):
        return_list = []
        for i in range(4):
            with open(f"symptom_files/symptoms{i}.txt", "r") as symptom_file:
                all_lines = symptom_file.readlines()
                for line in all_lines:
                    line = line.replace('"', "").strip().replace("_", " ")
                    line = line.split(",")
                    #print("list line -> ", str(line[0]).strip().lower())
                    #print("symptom line -> ", str(symptom).strip().lower())
                    if str(line[0]).strip().lower() == str(symptom).strip().lower():
                        return_list = line[1:]
        return return_list

    data_list = []
    # Put in JSON format
    for symptom in symptoms:
        formatted_symptom = str(symptom).strip().replace("_", " ")
        data_list.append({
            "tag":  formatted_symptom,
            "patterns": form_pattern(formatted_symptom),
            "responses": form_response(formatted_symptom),
            "context_set": ""
        })

    # Wrap the data in the "intents" tag
    json_data = {"intents": data_list}

    with open('intents.json', 'w') as outfile:
        json.dump(json_data, outfile)
