#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
from splinter import Browser
import re
import time
import pandas as pd


# In[2]:

def scrape_all():
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path)


    # In[3]:
    first_title, first_paragraph = mars_news(browser)
    
    # Run the functions below and store into a dictionary
    results = {
        "title": first_title,
        "paragraph": first_paragraph,
        "image_URL": featured_image(browser),
        "weather": twitter_weather(browser),
        "facts": fact(browser),
        "hemispheres": scrape_hemisphere(browser)
    }

    # Quit the browser and return the scraped results
    browser.quit()
    return results

def mars_news(browser): 
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    
   
    #response = requests.get(url)    

    #create BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    slide_elem= soup.select_one('ul.item_list li.slide')
    slide_elem.find("div", class_='content_title')
    # get the text
    news_title = slide_elem.find("div", class_='content_title').get_text()
    news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    browser.quit()
    return news_title, news_p


# In[4]:


    # news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    # news_p


# In[5]:

def featured_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    full_image_elem=browser.find_by_id("full_image")
    full_image_elem.click()
    #find more info
    browser.is_element_present_by_text("more info",wait_time=0.5)
    featured_image_url = browser.find_link_by_partial_text("more info")
    featured_image_url.click()

    html=browser.html
    img_soup = BeautifulSoup(html, "html.parser")
    img=img_soup.select_one("figure.lede a img")

    try:
        img_url_rel= img.get("src")
        
    except AttributeError:
        return None

    img_url=f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url





# In[6]:

def twitter_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)
    html = browser.html

    weather_soup = BeautifulSoup(html, 'html.parser')
    mars_weather_tweet=weather_soup.find('div', attrs={"class":"tweet", "data-name": "Mars Weather"})

    try:
        mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()

    except AttributeError:
        pattern=re.compile(r'sol')
        mars_weather=weather_soup.find('span',text=pattern).text

    return mars_weather


# In[7]:

def fact(browser):
    url = 'https://space-facts.com/mars/'  
    try:
        table = pd.read_html(url)
        mars_facts = table[0]

    except BaseException:
        return None
    
    facts = mars_facts.to_html()

    
    return facts


# In[11]:

def scrape_hemisphere(browser):
    hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(5)
    html=browser.html

    hemisphere_soup= BeautifulSoup(html, 'html.parser')

    hemisphere_links = []
    try:
        links=hemisphere_soup.find_all('h3')
    except AttributeError:
        links= None

    for link in links:
        hemisphere_links.append(link.text)


# In[12]:


    hem_url = []

    for image in hemisphere_links:
        hemispheres = {}
        browser.click_link_by_partial_text('Enhanced')
        time.sleep(5)
        try:
            hemispheres['image_url'] = browser.find_by_text('Sample')['href']
            hemispheres['title'] = image
        except AttributeError:
            hemispheres['image_url'] = None
            hemispheres['title'] = None

        hem_url.append(hemispheres)
    return (hem_url)


# In[ ]:




