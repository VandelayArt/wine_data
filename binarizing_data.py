import torch
import pandas as pd
import nltk

from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tag.util import untag
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer

import string

# Loading data
wine_data = pd.read_csv('wine_profile_databank.csv')
print(wine_data)

dummy1 = pd.get_dummies(wine_data['acidity'])
dummy2 = pd.get_dummies(wine_data['alcohol_percentage'])
dummy3 = pd.get_dummies(wine_data['body'])
dummy4 = pd.get_dummies(wine_data['sweetness'])
dummy5 = pd.get_dummies(wine_data['tannins'])

# Acidity

# Tokenize as sentences
for acid in dummy1:
    tokenized1 = nltk.sent_tokenize(acid)
    tokenized1
# Binarizing through concatenation
binary_acidity = pd.concat((wine_data, dummy1), axis=1, join='outer')
# Testing the function
print(binary_acidity.head())

# Same steps apply also apply for the dummy elements

# Alcohol

for alcohol in dummy2:
    tokenized2 = nltk.sent_tokenize(alcohol)
    tokenized2

binary_alcohol = pd.concat((wine_data, dummy2), axis=1, join='outer')

print(binary_alcohol.head())


# Body
for body in dummy3:
    tokenized3 = nltk.sent_tokenize(body)
    tokenized3

binary_body = pd.concat((wine_data, dummy3), axis=1, join='outer')

print(binary_body.head())


# Sweetness
for sweety in dummy4:
    tokenized4 = nltk.sent_tokenize(sweety)
    tokenized4

binary_sweetness = pd.concat((wine_data, dummy4), axis=1, join='outer')

print(binary_sweetness.head())


# Tannins
for tannin in dummy5:
    tokenized5 = nltk.sent_tokenize(tannin)
    tokenized5

binary_tannin = pd.concat((wine_data, dummy5), axis=1, join='outer')

print(binary_tannin.head())
