# Dataset Processing

## [The Dataset.](https://www.kaggle.com/itachi9604/disease-symptom-description-dataset)
There are 4 datasets, the main one that we'll be using is `dataset.csv`. `symptom_precation.csv` might be useful too (for making recommendations).

## intents.json
This is the file that a NLTK model (the nat. language model) is trained on. We put the `dataset.csv` into this format.

The format looks like this (for the current basic model):

```{"intents": [
        {"tag": "greeting",
         "patterns": ["Hi", "How are you", "Is anyone there?", "Hello", "Good day", "Whats up"],
         "responses": ["Hello!", "Good to see you again!", "Hi there, how can I help?"],
         "context_set": ""
        },


	**.....**


	{"tag": "hours",
         "patterns": ["when are you guys open", "what are your hours", "hours of operation"],
         "responses": ["We are open 7am-4pm Monday-Friday!"],
         "context_set": ""
        }
   ]
}
```

We're going to want it to look something like this:

```{"intents": [
        {"tag": "coughing",
         "patterns": ["I've been coughing", "I have a cough", "I've got a cough"],
         "responses": ["You've got a cough? Ok.", "Alright, a cough. Anything else?", "A cough, okay, any other symptoms?"],
         "context_set": ""
        },


	**.....**


	{"tag": "sore throat",
         "patterns": ["I've got a sore throat", "My throat hurts", "My throat is sore"],
         "responses": ["Ok, you've got a sore throat, anything else."],
         "context_set": ""
        }
   ]
}
```

(Or something like this).

## Things to do:

* First of all, I think (to begin with, at least) we should narrow the down the number of illnesses. Maybe find a list of the most common ones?
* Then parse through the dataset and make each symptom into a "tag".
* Then write a function for making some responses to the symptom - e.g. "Alright, you've got {symptom}, anything else?". Once some responses have been made, put that into the "responses" for each symptom.
* Then comes the boring part: I think we will have to manually write some patterns that indicate a symptom, and put them in the "patterns" section.
* Once this has been done, we can move on to the next Nat. Lang part.

## Notes:
* The format of the `intents.json` file is JSON, look into it.
* **We do not want to be doing this manually, it would be so boring.**


