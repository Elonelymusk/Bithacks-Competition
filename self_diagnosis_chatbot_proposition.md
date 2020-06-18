# This is the way I was thinking of making the self-diagnosis chatbot.

## The dataset:
Here's a dataset that I found simply from a cursory look, but I'm sure there are better options.
https://www.kaggle.com/itachi9604/disease-symptom-description-dataset?select=dataset.csv

## An example:
Let's say, for the sake of example and relative simplicity we want to discern between `common cold`, `allergy`, `pneumonia`, `tuberculosis` and `Asthma`.

 *	Common cold symptoms:	continuous sneezing, chills, fatigue, cough, high fever, headache, phlegm.
 *	Allergy symptoms:	continuous sneezing, shivering, chills, watering from eyes.
 * 	Pneumonia symptoms:	chills, fatigue, cough, high fever, breathlessness, sweating, phlegm, chest pain.
 * 	Tuberculosis symptoms:	chills, vomiting, fatigue, weight loss, cough, high fever, breathlessness, sweating, loss of appetite.
 * 	Asthma symptoms:	fatigue, cough, high fever, breathlessness, family history, mucoid sputum.

## The method:
It would start out with a greeting:

`Bot	->	'Hi, I'm the self-diagnosis chatbot. I will aim to determine what illness you are suffering from based on your description of the your symptoms. So please describe how you're feeling.'`

Then the user would describe their symptoms. They might start by saying something meaningless, like:

`User	->	'Hello, I'm feeling really ill.'`
`Bot	->	'Oh, I'm sorry to hear that, could you describe any specific symptoms?'`

Hopefully then, the user would start listing out their symptoms:

`User	->	'I've got a terrible cough.'`
`Bot   	-> 	'Okay, anything else?'`

At this point, the bot will be able to determine that this is likely worse than just allergies, as the `allergy` symptoms do not contain `cough`.

`User	->	'I've been feeling really cold.'`
`Bot 	->	'Hmm... Alright, any other symptoms?'`

At this point, `asthma` has been deemed less likely, as it doesn't have `chills` or `shivering`.

`User	->	'I've also been sneezing a lot.'`
`Bot	->	'Oh, okay. Anything else?'`

This increases the likelyhood of it being `common cold` or `allergy`. Now let's suppose that the user doesn't really have any more symptoms to list.

`User	->	'Not really.'`
`Bot	->	'Alright, do you mind if I ask any questions?'`
`User	->	'Sure.'`

Now the bot has to chose **useful** questions to ask.

`Bot	->	'Have you been feeling more tired than usual?'`
`User	->	'Yes actually, I've felt quite lethargic.'`
`Bot	->	'Okay, Have you felt particularly breathless?'`
`User	->	'No, not really.'`

An arbitrary number of questions could be asked, but lets just suppose for the sake of simplicity, that we're only asking 2. Now we have gathered enough data to make an educated guess:

 *	It's probably `common cold`, most of the symptoms match up.
 * 	It could be `asthma`, as although the symptoms don't all match, a significant number do.
 *  	It is highly unlikely to be `tuberculosis`, not only because the symptoms don't really match up, but because it's also pretty uncommon.

The bot would then relay this to the user.

## Main Problems (as far as I see them):
 *	The actual understanding of what the user is saying is pretty non-trivial.
 *	We have to account for the user saying things that aren't really related to the symptoms, otherwise the model might get confused.
 * 	I think we're going to have to combine a few datasets in order to get a good sample of data.





