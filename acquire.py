#######################################################
# This file is for the acquire exercises for NLP codeup module.
#######################################################

#imports
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
import os

def get_codeup_articles(url):
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

def get_blog_articles_data(refresh=False):
    """This function is from our class tutorial. It goes through
    all of the acquire exercises for the nlp exercises"""

    if not os.path.isfile('blog_articles.csv') or refresh:

        url = 'https://codeup.com/blog/'
        headers = {'User-Agent': 'Codeup Data Science student'}
        response = get(url, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        links = [link['href']for link in soup.select('h2 a[href]')]

        articles = []

        for url in links:

            url_response = get(url, headers=headers)
            soup = BeautifulSoup(url_response.text, 'html.parser')

            title = soup.find('h1', class_='entry-title').text
            content = soup.find('div', class_='entry-content').text.strip()

            article_dict = {
                'title': title,
                'content': content
            }

            articles.append(article_dict)

        blog_article_df = pd.DataFrame(articles)

        blog_article_df.to_csv('blog_articles.csv', index=False)

    return pd.read_csv('blog_articles.csv')


def parse_news_article(article, category):
    """this function pulls inshorts news articles and reassigns the tile and content of the articles
    by categoryinto a dicitionary"""
    
     #creating the dictionary
    output = {}
    
    output['title'] = article.find("span", itemprop = "headline").text.strip()
    output['content'] = article.find("div", itemprop = "articleBody").text
    output['author'] = article.find("span", class_ = "author").text
    output['date'] = article.find("span", class_ = "date").text
    output['source'] = article.find("a", class_ = "source")
    output['category'] = category
    
    return output

#### Modifying the above to dictionary all articles into one page:

def parse_news_page(category):
    url = "https://inshorts.com/en/read/"+category
    response = get(url)
    soup = BeautifulSoup(response.text)
    
    cards = soup.select('.news-card')
    articles = []
    
    for card in cards:
        articles.append(parse_news_article(card, category))
        
    return articles



def get_news_articles(use_cache = True):
    """creating one function that grabs all categories and 
    puts them into one dictionary, while adding a cache of the data:"""
    if os.path.exists('news_articles.json') and use_cache:
        return pd.read_json('news_articles.json')
    
    categories = ['business', 'sports', 'technology', 'entertainment']
    
    articles = []
    
    for category in categories:
        print(f'Getting {category} articles')
        articles.extend(parse_news_page(category))
        
    df = pd.DataFrame(articles)
    df.to_json('news_articles.json', orient ='records')
    return df

