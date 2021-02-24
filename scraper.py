import requests
from bs4 import BeautifulSoup

import nltk
import pandas as pd

import re

from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tag.util import untag
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer

import string

#Grape Vocabulary cleaned and fitted for winefolly links
grapes_test = pd.read_csv('grape_names.csv')
grapes_split = [tags.split(',') for tags in grapes_test['Grapes'].values]
grapes_joined = ["".join(word) for word in grapes_split]


#Storing the lemmatizer as a variable
wordnet_lemmatizer = WordNetLemmatizer()

#Dictionaries to write to pandas DF from scrape
grape_dict = []
dominant_flavor_dict = []
grape_taste_sweetness_dict = []
grape_taste_body_dict = []
grape_taste_tannins_dict = []
grape_taste_acidity_dict = []
grape_taste_alcohol_dict = []
raw_food_pairing_dict = []

grape_food_pairing_dict = []

wine_profile_databank = []


def __main__():
    # Setting up the scrape urls  
    URL = 'https://winefolly.com/grapes/grape_query/'
    new_url_List = [re.sub('grape_query', word, URL) for word in grapes_joined]

    # Looping through the url list
    for url in new_url_List:
    # Creating a profile to write to a database later
        wine_profile = []
        try:
    # Parsing the html page with BeautifulSoup    
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

    # Choosing the base soup element to scrape from
            grapies = soup.find('div', class_='col-12')

    # Finding the name of the grape and storing it in the appropriate dictionary
            grape_name = grapies.find('h1', class_='px-5')
            grape_variety = grape_name.text.strip()
            variety_lc = grape_variety.lower()
            wine_profile.append([variety_lc])


    # Finding the dominant flavours and storing it in the appropriate dictionary
            flavors = soup.find(id='flavours')
            flavor_elems = flavors.find_all('ul', class_='flavours')

            dominant_flavors = []

            for flavor_elem in flavor_elems:
                item_elems = flavor_elem.find_all('li')
                if None in item_elems:
                    continue
                else:
                    for item_elem in item_elems:
                        name_elem = item_elem.find('span')
                        grape_flavors = (name_elem.text)
                        dominant_flavor_dict.append([grape_flavors.lower()])
                        dominant_flavors.append([grape_flavors.lower()])


    # Finding the taste profile elements and storing them in the appropriate dictionary
            taste_profile = soup.find(id='tasting-profile')
            taste_profile_elems = taste_profile.find_all('div')

            grape_taste_profile = []

            for taste_profile_elem in taste_profile_elems:
                taste_sweetness = taste_profile_elem.find(class_='label sweetness')
                taste_body = taste_profile_elem.find(class_='label body')
                taste_tannins = taste_profile_elem.find(class_='label tannins')
                taste_acidity = taste_profile_elem.find(class_='label acidity')
                taste_alcohol = taste_profile_elem.find(class_='label alcohol')
                if None in (taste_sweetness, taste_body, taste_tannins, taste_acidity, taste_alcohol):
                    continue
                else:
                    acidity = taste_acidity.text.strip()
                    grape_taste_acidity_dict.append([acidity.lower()])
                    grape_taste_profile.append([acidity.lower()])
                    
                    alcohol = taste_alcohol.text.strip()
                    grape_taste_alcohol_dict.append([alcohol])
                    grape_taste_profile.append([alcohol])

                    body = taste_body.text.strip()
                    grape_taste_body_dict.append([body.lower()])
                    grape_taste_profile.append([body.lower()])
                    
                    sweetness = taste_sweetness.text.strip()
                    grape_taste_sweetness_dict.append([sweetness.lower()])
                    grape_taste_profile.append([sweetness.lower()])
                    
                    tannins = taste_tannins.text.strip()
                    grape_taste_tannins_dict.append([tannins.lower()])
                    grape_taste_profile.append([tannins.lower()])

    # Finding the food pairings, and cleaning them (tokenizing, lowercasing, removing punctuation, 
    # lemmatizing, removing duplicates, tagging, chunking,  storing it in the appropriate dictionary
            food_pairing = soup.find(id='food-pairing')
            food_pairing_elems = food_pairing.find_all('p')

            wine_pairing = []

            if None in food_pairing_elems:
                continue
            else:
                for food_pairing_elem in food_pairing_elems:
                    raw_food_pairing = food_pairing_elem.text
    # Tokenize the words
                    tokens = word_tokenize(raw_food_pairing)
    # Make all tokens lowercase
                    tokens = [word.lower() for word in tokens]
    # Remove punctuation
                    table = str.maketrans('', '', string.punctuation)
                    stripped = [w.translate(table) for w in tokens]

    # Remove stopwords with Wordnet Library
                    words = [word for word in stripped if word.isalpha()]
                    stop_words = set(stopwords.words('english'))
                    words = [w for w in words if not w in stop_words]
                    words

    # Removing grapes from cleaned grape vocabulary I built in CSV
                    new_words = [w for w in words if not w in grapes_joined]
                    new_words

    # Lemmatize the words
                    lemmatized = [wordnet_lemmatizer.lemmatize(word) for word in new_words]
    
    # Filter the lemmatized list and remove duplicates without loosing order
                    duplicates_removed = []
                    for word in lemmatized:
                        if word not in duplicates_removed:
                            duplicates_removed.append(word)
    
    # Add pos_tags to filtered words
                    tagged = nltk.pos_tag(duplicates_removed)
    
    #Chunking Technique selecting specific grammar types for this content
                    chunkGram = r"""ideal_pairing: {<IN>+<NN>|<JJ>+<JJ>+<NN>|<JJ>+<NN>+<NNS>|<JJ>+<NN>|<JJ>+<NNS>|<JJ>+<VBV>+<NN>|<JJ>|<JJR>+<NN>|<JJS>|<NN>|<NN>+<JJ>|<NN>+<NNS>|<NN>+<VBD>|<NN>+<VBP>|<NNP>|<RB>+<VBN>+<NN>|<RB>+<VB>|<VBD>+<JJ>+<NN>|<VBD>+<JJ>|<VBD>+<JJR>|<VBD>+<NN>|<VBN>+<NN>|<VBP>+<JJ>+<NN>|<VBP>+<NN>}
                    """
                    chunkParser = nltk.RegexpParser(chunkGram)
                    chunked = chunkParser.parse(tagged)

    # Isolating the appropriate chunks as ideal_pairing
                    chunky = chunked.subtrees(filter=lambda t: t.label() == 'ideal_pairing')
                    for subtrees in chunky:
                        pairing_dishes = subtrees.leaves()
                        untagged_dishes = untag(pairing_dishes)
                        raw_food_pairing_dict.append(pairing_dishes)
                        grape_food_pairing_dict.append(untagged_dishes)
                        wine_pairing.append(untagged_dishes)
            
            wine_profile.append(dominant_flavors)
            wine_profile.append(grape_taste_profile)
            wine_profile.append(wine_pairing)            
        
        except:
            print("-----", url, " -- Didn't work-----------------------------------------------------------------------")
        finally:
            print("-----", url, " --Worked Well------------------------------------------------------------------------")

            print(wine_profile)
            wine_profile_databank.append(wine_profile)
        
            
    # Reviewing the output in lists
    print("-----Grape Dictionary: ------------------------------------------------------------------------------------")
    print(grape_dict)
    print("")
    print(len(grape_dict))
    print("-----Dominant Flavor Dictionary: ------------------------------------------------------------------------------------")
    print(dominant_flavor_dict)
    print("")
    dominant_flavor_vocab = pd.DataFrame(data=dominant_flavor_dict, columns=['dominant flavors'])
    dominant_flavor_vocab.to_csv('grape_dominant_flavors_vocab.csv')
    print(len(dominant_flavor_dict))
    print("-----Grape Sweetness Dictionary: ------------------------------------------------------------------------------------")
    print(grape_taste_sweetness_dict)
    print("")
    grape_sweetness_vocab = pd.DataFrame(data=grape_taste_sweetness_dict, columns=['sweetness_vocab'])
    grape_sweetness_vocab.to_csv('grape_sweetness_vocab.csv')
    print(len(grape_taste_sweetness_dict))
    print("-----Grape Body Dictionary: ---------------------------------------------------------------------------------------")
    print(grape_taste_body_dict)
    print("")
    grape_body_vocab = pd.DataFrame(data=grape_taste_body_dict, columns=['body_vocab'])
    grape_body_vocab.to_csv('grape_body_vocab.csv')
    print(len(grape_taste_body_dict))
    print("-----Grape Tannins Dictionary: ------------------------------------------------------------------------------------")
    print(grape_taste_tannins_dict)
    print("")
    grape_tannins_vocab = pd.DataFrame(data=grape_taste_tannins_dict, columns=['tannins_vocab'])
    grape_tannins_vocab.to_csv('grape_tannins_vocab.csv')
    print(len(grape_taste_tannins_dict))
    print("-----Grape Acidity Dictionary: ------------------------------------------------------------------------------------")
    print(grape_taste_acidity_dict)
    print("")
    grape_acidity_vocab = pd.DataFrame(data=grape_taste_acidity_dict, columns=['acidity_vocab'])
    grape_acidity_vocab.to_csv('grape_acidity_vocab.csv')
    print(len(grape_taste_acidity_dict))
    print("-----Grape Alcohol Dictionary: ------------------------------------------------------------------------------------")
    print(grape_taste_alcohol_dict)
    print("")
    grape_alcohol_vocab = pd.DataFrame(data=grape_taste_alcohol_dict, columns=['alcohol_vocab'])
    grape_alcohol_vocab.to_csv('grape_alcohol_vocab.csv')
    print(len(grape_taste_alcohol_dict))
    print("-----Raw Food Pairing Dictionary: ---------------------------------------------------------------------------------")
    print(raw_food_pairing_dict)
    print("")
    print(len(raw_food_pairing_dict))
    print("-----Food Pairing Dictionary: -------------------------------------------------------------------------------------")
    print(grape_food_pairing_dict)
    print("")
    print(len(grape_food_pairing_dict))
    print("-----Wine Profile Databank: ---------------------------------------------------------------------------------------")
    print(wine_profile_databank)
    print("")
    wine_profile_db = pd.DataFrame(data=wine_profile_databank, columns=['grape_name', 'dominant_flavors', 'taste_profile', 'food_pairings'])
    wine_profile_db.to_csv('wine_profile_db.csv')
    print(len(wine_profile_databank))
    print(wine_profile_db.head())



    
if __name__ == '__main__':
    __main__()