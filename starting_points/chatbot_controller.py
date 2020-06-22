from nltk_lib import prep_dataset, build_model, response
import pickle

# Create the model
prep = prep_dataset()

words = prep[0]
classes = prep[1]
train_x = prep[2]
train_y = prep[3]

build_model(train_x, train_y)

# Store the important variables to a .pickle file
with open('train.pickle', 'wb') as file:
    pickle.dump([words, classes], file)

