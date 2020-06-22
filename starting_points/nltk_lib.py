import nltk
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import random
import pickle
from nltk.stem.lancaster import LancasterStemmer
import json

# Prepare the dataset and important variables
def prep_dataset():
    nltk.download('punkt')

    stemmer = LancasterStemmer()

    # Import our chatbot intents file
    with open('intents.json') as json_data:
        intents = json.load(json_data)

    words = []
    classes = []
    documents = []
    ignore_words =['?']

    # Loop through each sentence in intents pattern
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            w = nltk.word_tokenize(pattern)
            words.extend(w)
            documents.append((w,intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    # Stem and lower each word and remove duplicates
    words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
    words = sorted(list(set(words)))

    # Remove duplicates
    classes = sorted(list(set(classes)))

    training = []
    output = []
    # Create an empty array for our output
    output_empty = [0] * len(classes)

    # Training set, bag of words for each sentence
    for doc in documents:
        bag = []
        pattern_words = doc[0]
        pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)

        # Output is a zero for each tag and 1 for current tag
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1

        training.append([bag, output_row])

    # Shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)

    # Create training and testing lists
    train_x = list(training[:,0])
    train_y = list(training[:,1])

    return [words, classes, train_x, train_y]

# Build neural network
def build_model(train_x, train_y):
    model = models.Sequential()
    model.add(layers.Flatten())
    model.add(layers.Dense(8, input_shape = [None,len(train_x[0])]))
    model.add(layers.Dense(8))
    model.add(layers.Dense(len(train_y[0]), activation='softmax'))

    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    model.fit(train_x, train_y,batch_size= 8, epochs=1000)

    # I think it would be better just to build the model once and then load it later
    model.save('built_model')

# Tokenize the sentence and stem each word
def clean_up_sentence(sentence):
    stemmer = LancasterStemmer()
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# Return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details = False):
    # Tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # Create a BOW
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))

# Build the response processor
context = {}
ERROR_THRESHOLD = 0.25
def classify(sentence, words, classes):
    new_model = tf.keras.models.load_model('./built_model')
    # Generate probabilities from the model
    results = new_model.predict(np.array([bow(sentence,words)]))[0]
    # Filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r> ERROR_THRESHOLD]
    # Sort by strength of probability
    results.sort(key = lambda x: x[1], reverse =True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list

def response(words, classes, sentence, userID='123', show_details=False):
    results = classify(sentence, words, classes)
    with open('intents.json') as json_data:
        intents = json.load(json_data)
    # If we have a classification then the matching intent tag
    if results:
        # Loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                if i['tag'] == results[0][0]:
                    # A random response from the intent
                    if 'context_set' in i:
                        if show_details: print('context:', i['context_set'])
                        context[userID] = i['context_set']

                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter']==context[userID]):
                        if show_details: print('tag:', i['tag'])

                        return print(random.choice(i['responses']))

            results.pop(0)
