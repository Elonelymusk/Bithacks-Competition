from data_preparation import process_dataset
from nltk_lib import prep_model, build_model, response

# Create the model
print("Preparing the model...\n")
process_dataset()
prep = prep_model()

words = prep[0]
classes = prep[1]
train_x = prep[2]
train_y = prep[3]
print("...Model prepared.\n")
print("Building model...\n")
build_model(train_x, train_y)
print("...Model built.\n")

#Test the model
response(words, classes, "I'm really itchy.")
response(words, classes, "I'm losing weight")
response(words, classes, "I feel dizzy")