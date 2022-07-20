#########################################
# This file holds the prepare functions for the NLP exercises found in Codeup's 
# curriculum.
#########################################

import pandas as pd
from nltk.corpus import stopwords


import re
import unicodedata
import pandas as pd
import nltk

def basic_clean(string):
    """A function that uses NLTK to clean and normalizes a string"""
    string = string.lower()
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    string = re.sub(r"[^a-z0-9'\s]", '' ,string)
    return string

def tokenize(string):
    """This function will take in a string, tokenize by breaking any leftover words into units and return 
    the tokenized string"""
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    string = tokenizer.tokenize(string, return_str=True)
    return string

def stem(string):
    """This function takes in a string and returns the stemmed version of string"""
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    string = ' '.join(stems)
    
    return string

def lemmatize(string):
    """This function takes in a string and returns a lemmatized version of the string."""
    # create our lemmatizer object
    wnl = nltk.stem.WordNetLemmatizer()
    # use a list comprehension to lemmatize each word
    # string.split() => output a list of every token inside of the document
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    # glue the lemmas back together by the strings we split on
    string = ' '.join(lemmas)
    #return the altered document
    return string

def remove_stopwords(string, extra_words = [], exclude_words = []):
    """This function takes in a string, applies stop_words to take out common stop words, includes any extra words
    wanted removed and excludes and stop words wanted kept"""
    #assign stopwords from nltk into a stopword_list:
    stopword_list = stopwords.words('english')
    #remove any excluded stopwords that are wanted to be kept:
    stopword_list = set(stopword_list) - set(exclude_words)
    #add on any other stopwords using a union
    stopword_list = stopword_list.union(set(extra_words))
    #split the words by spaces
    words = string.split()
    #filter out every word in dict unless in stop word:
    filtered_words = [word for word in words if word not in stopword_list]
    #put it back together with spaces
    string_without_stopwords = ' '.join(filtered_words)
    #return df back
    return string_without_stopwords

#creating function of above needed items:
def prep_article_data(df, column, ignore_columns = [], extra_words=[], exclude_words=[]):
    '''
    This function takes in a df and the string name for a text column with the
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords,
                                  extra_words=extra_words,
                                  exclude_words=exclude_words)
    
    df['stemmed'] = df['clean'].apply(stem)
    
    df['lemmatized'] = df['clean'].apply(lemmatize)

    cleaned_columns = [column, 'clean','stemmed','lemmatized']
    all_columns = ignore_columns + cleaned_columns


    return df[all_columns]






