import os.path
import json
from os import path
import pandas as pd
from nltk_lib import prep_model, build_model, response
from yn_lib import prep_yn_model, build_yn_model, yn_response
from data_preparation import process_dataset

# Function to give a response to a symptom prompt
def give_response(message):
    # Gather the data
    process_dataset()
    prep = prep_model()
    words = prep[0]
    classes = prep[1]
    train_x = prep[2]
    train_y = prep[3]
    
    # If the model is built, don't build it again
    if path.exists("built_model/") == True:
        resp_string = response(words, classes, message)
    else:
        # Since model isn't built, build model
        build_model(train_x, train_y)
        resp_string = response(words, classes, message)

    return resp_string

# Determine whether the user replied 'yes' or 'no' to the question
def yes_no_response(message):
    # Gather the data
    prep = prep_yn_model()
    words = prep[0]
    classes = prep[1]
    train_x = prep[2]
    train_y = prep[3]
    
    # If the model is built, don't build it again
    if path.exists("built_yn_model/") == True:
        resp_string = yn_response(words, classes, message)
    else:
        # Since model isn't built, build model
        build_yn_model(train_x, train_y)
        resp_string = yn_response(words, classes, message)

    return resp_string

# The chat loop
def start_chat():
    start_message = "Hello, I am the CSFC Symptom Chatbot.\nMy aim is to diagnose the illness you are suffering from, based on the symptoms that you describe to me.\nDISCLAIMER: It is important to note that I am merely a work-in-progress and if you feel that you need to consult a doctor, do so.\n\nAnyway, please begin by describing the symptoms that you have.\n\n"
    print(start_message)
    chat_flag = True
    symptom_list = []
    while chat_flag == True:
        user_input = input(">>>     ")
        response = give_response(user_input)
        if response == None:
            print("Sorry, I didn't understand that. Please try again.")
        elif "quit" in response:
            print("Okay, I'm going to ask you a few questions now.")
            chat_flag = False
        else:
            print(response)
            symptom = response.replace("'ve detected ", "").split("'")[1]
            symptom_list.append(symptom)
    print(symptom_list)
    return symptom_list

# Ask a question
def ask_question(symptom):
    with open("intents.json", "r") as json_file:
        intents = json.load(json_file)
        intents_list = intents['intents']
        symp_dict = {}
        for element in intents_list:
            #print("symptom -->", symptom)
            #print(element['tag'])
            if symptom == element['tag']:
                symp_dict = element
        print(symp_dict)
        patterns = symp_dict['patterns']
        for i in range(len(patterns)):
            if i != len(patterns) - 1:
                patterns[i] = patterns[i] + '. ' + '----- '
            else:
                patterns[i] = patterns[i] + '.'  
        question = 'Do any of these describe you well? -> ' + "".join(patterns)
        return question

# The question loop
def questions(symptoms):
    dataframe = pd.read_csv('dataset.csv')

    # First, remove the illnesses that are obviously incorrect.
    correct_dict = {}
    incorrect_dict = {}
    illness_columns = dataframe.columns

    # Initiate the dictionaries that dictate the number of correct or incorrect 'tokens' each illness has
    for column in illness_columns:
        correct_dict[column] = 0
        incorrect_dict[column] = 0
        contents = list(dataframe[column])
        stripped_contents = []
        for element in contents:
            stripped_contents.append(element.strip())
        for a_symptom in symptoms:
            if a_symptom in stripped_contents:
                correct_dict[column] += 1
            else:
                incorrect_dict[column] += 1
    for illness in correct_dict:
        # The parameters used here are somewhat arbitrary, they may have to be tuned
        if correct_dict[illness] == 0 and incorrect_dict[illness] > 2:
            correct_dict[illness] = None
            incorrect_dict[illness] = None
    correct_dict = {key:val for key, val in correct_dict.items() if val != None}
    incorrect_dict = {key:val for key, val in incorrect_dict.items() if val != None}

    # Now move on to the question asking part - currently restricted to 5 questions
    asked_list = []
    for _cycle in range(5):
        # Process:
        #   -   Find most common symptom between all of them
        #   -   Ask the user if this describes them
        #   -   Update accordingly
        #   -   Repeat
        
        # NB: CORRECTDICT IS EMPTY

        # Find most common symptom
        symptom_dict = {}
        for illness in correct_dict:
            contents = list(dataframe[illness])
            for symptom in contents:
                if symptom == "None" or symptom in symptoms or symptom in asked_list:
                    pass
                elif symptom in symptom_dict:
                    symptom_dict[symptom] += 1
                else:
                    symptom_dict[symptom] = 1
        greatest_value = 0
        greatest_symptom = ""
        for b_symptom in symptom_dict:
            if symptom_dict[b_symptom] > greatest_value:
                greatest_value = symptom_dict[b_symptom]
                greatest_symptom = b_symptom
        
        # Ask whether the user has experienced any of the symptoms
        print(ask_question(greatest_symptom.strip().replace("_", " ")))
        user_input = input(">>>     ")
        response = str(yes_no_response(user_input))
        print(response)

        # Add correct / incorrect tokens where necessary:
        if "no" in response.lower():
            for correct_illness in correct_dict:
                contents = list(dataframe[correct_illness])
                if greatest_symptom in contents:
                    incorrect_dict[correct_illness] += 1
        elif "yes" in response.lower():
            for correct_illness in correct_dict:
                contents = list(dataframe[correct_illness])
                if greatest_symptom in contents:
                    correct_dict[correct_illness] += 1
        asked_list.append(greatest_symptom)

    # Make decision and return information based on this - return the illnesses in order of likelyhood
    decision_dict = correct_dict
    decision_list = []
    for illness in decision_dict:
        decision_dict[illness] = (correct_dict[illness] * 2) - incorrect_dict[illness]
     
    for i in range(len(decision_dict)):
        greatest_val = -100
        greatest_illness = ""
        for dec_illness in decision_dict:
            if decision_dict[dec_illness] > greatest_val and dec_illness not in decision_list:
                greatest_val = decision_dict[dec_illness]
                greatest_illness = dec_illness
        decision_list.append(greatest_illness)

    for i in range(len(decision_list)):
        print(str(i+1), ": ", decision_list[i])
    
    return decision_list
            
#questions(["skin_rash", "itching", "fatigue", "continuous_sneezing"])
questions(start_chat())   