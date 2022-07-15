#######################################################
# This file is for the acquire exercises for NLP codeup module.
#######################################################

#imports
import pandas as pd
from requests import get
from bs4 import BeautifulSoup

def get_blog_articles(url):
    """this function pulls codeup blog urls and reassigns the tile and content of the blog
    into a dicitionary"""
    url = url
    #establishing a header for access:
    headers = {'User-Agent': 'Codeup Data Science Student'} 
    response = get(url, headers=headers)
    
    # Make a soup variable holding the response content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    #creating the dictionary
    output = {}
    output['title'] = soup.find('h1', class_='entry-title').text
    output['content'] = soup.find('div', class_='entry-content').text.strip().replace('\n',' ')
    
    return output


