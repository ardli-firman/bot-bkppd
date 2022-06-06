from numpy import size
from sklearn.naive_bayes import MultinomialNB # classifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer # text vectorizer
#from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score  # evaluation
 
import matplotlib.pyplot as plt # visualization
import pandas as pd # data representation
from sklearn.pipeline import make_pipeline
from sklearn.metrics import plot_confusion_matrix
import pandas as pd

import json
import string

intent = open('data/intents.json')
data = json.load(intent)

 
text_input = []
kelas = []
for i in data['intents']:
    for y in i['patterns']:
        text_input.append(y.lower().translate(str.maketrans("","",string.punctuation)))
        kelas.append(i['tag'].lower().translate(str.maketrans("","",string.punctuation)))

df = pd.DataFrame({'text_input':text_input,'kelas': kelas})

train_data = (list(df['text_input']))
train_target = (list(df['kelas']))
  

tfidf = TfidfVectorizer()
vectorizer = tfidf.fit_transform(train_data)
data = pd.DataFrame(vectorizer.toarray(), columns=tfidf.get_feature_names_out())


count_vector = CountVectorizer()
vectorizer = count_vector.fit_transform(train_data)
data = pd.DataFrame(vectorizer.toarray(), columns=count_vector.get_feature_names_out())


model_tfidf = make_pipeline(TfidfVectorizer(), MultinomialNB())
model_count = make_pipeline(CountVectorizer(), MultinomialNB())

model_tfidf.fit(train_data, train_target)
model_count.fit(train_data, train_target)
#y_pred_tfidf = model_tfidf.predict(test.data)
#y_pred_count = model_count.predict(test.data)

#f1 = f1_score(test.target, y_pred_tfidf, average='weighted')
#accuracy = accuracy_score(test.target, y_pred_tfidf)

text = [
    'absen tidak bisa'
]

y_pred = model_tfidf.predict(text) 
print(y_pred)

#for i in range(len(y_pred)):
#   print(f'"{target_categories[y_pred[i]]:<22}" ==> "{text[i]}"')




