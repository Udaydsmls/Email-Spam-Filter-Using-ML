import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
from nltk.corpus import stopwords
import string

df = pd.read_csv("spam_ham_dataset.csv", encoding="latin-1")


def preprocess(text):
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)

    clean = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    return clean


df['label'] = df['label'].map({'ham': 0, 'spam': 1})
X = df['text']
y = df['label']

cv = CountVectorizer(analyzer=preprocess)
X = cv.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

clf = MultinomialNB()
clf.fit(X_train, y_train)
pred = clf.predict(X_test)
print(classification_report(y_test, pred))
print("Accuracy: \n", accuracy_score(y_test, pred))

joblib.dump(clf, 'Spam_Model_NB.pkl')
