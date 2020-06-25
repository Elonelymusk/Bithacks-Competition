# Bithacks-Competition
The AI-for-social-change hackathon.

## Self-diagnosis Chatbot:
We could make a chatbot website, in which the user describes their symptoms to the chatbot, and a model tries to determine what illness they have.

### **`Pros`:**
 *    There are plenty of simple tutorials for the constituent parts of this project. We could use these as a starting point.
 *    There are a few datasets that could be used for this project.

### **`Cons`:**
 *    Just like the 'Brain Tumour Detector' the medical obligation to make the model consistent is present.
 *    We will need to think about hosting the website, I (Guillaume) would be happy to do this, but it would cost some money.

## ToDo:
* Website:
- [x] Create a basic chatbot website.
- [ ] Link up the model to the website.
- [ ] Make it look good.
- [ ] Host the chatbot on a website (easy to do, but somewhat optional).
* Dataset Processing:
- [x] Decide on whether we need to combine a few datasets (or create our own).
- [x] Keep the things we want in the dataset, remove whatever we don't want.
- [x] Find a way of converting the dataset to an intents.json file. **<---- One of the main challenges.**
* Nat. Language Model:
- [x] Create a basic NLTK based Model.
- [x] Convert this model to use the new intents.json file.
- [ ] Optimize the model. **<---- One of the main challenges.**
* Diagnosis Making:
- [ ] Determine which illness the user is suffering from based on the symptoms. I'd suggest K-Nearest-Neighbors or K-Means algorithms. **<---- One of the main challenges.**

As I see it, the website can be improved upon at any time. The `Nat. Language Model` cannot be improved until the `intents.json` file has been made. The diagnosis making model could be worked upon by using the dataset we decide upon for testing.

**Based on this, the first thing to tackle will be the dataset processing.**

## Latest Upload:
* i've uploaded the two files for the brain tumor detector. If you guys want to have a go. change the path files within each python file. any path you see change it to your own
* please download the dataset first if you want to play around with the model you can find it here: https://www.kaggle.com/navoneel/brain-mri-images-for-brain-tumor-detection
* I've moved the brain tumour stuff to a sub-directory.
* I've written a description of what to do.
