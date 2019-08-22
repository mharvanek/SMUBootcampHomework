# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd
import time

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Select database and collection to use
db = client.mars_db
mars_info = db.mars_info


def init_browser():
    # set the chromedriver path
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    mars_news = scrape_mars_news()
    mars_feat_img = scrape_feat_img()
    #mars_fact = scrape_mars_facts

    # Store data in a dictionary
    mars_data = {
        "mars_news": mars_news,
        "mars_feat_img": mars_feat_img,
       # "mars_facts": mars_fact
    }

    return mars_data


def scrape_mars_news():

    mars_news = []

    # URL of page to be scraped
    mars_news_url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    mars_news_response = requests.get(mars_news_url)
    # Create BeautifulSoup object
    mars_news_html = BeautifulSoup(mars_news_response.text, 'html.parser')

    # Retrieve the parent divs for all articles
    results = mars_news_html.find_all('div', class_='slide')

    # Loop through results to retrieve article title, header, and timestamp of article
    for result in results:
        news_t = result.find('div', class_='content_title').find('a').text.strip()

        news_p = result.find('div', class_='rollover_description_inner').text.strip()

        mars_news.append({'title': news_t, 'news': news_p})

    return mars_news

def scrape_feat_img():
    
    browser = init_browser()

    # Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    jpl_base_url = 'https://www.jpl.nasa.gov'
    mars_images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_images_url)

    time.sleep(5)

    xpath = '//footer//a[@id="full_image"]'

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    results = browser.find_by_xpath(xpath)
    mars_feat_image = results[0]
    mars_feat_image.click()

    # Scrape the browser into soup and use soup to find the full resolution image of mars
    #assign the url string to a variable called `featured_image_url`.
    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = jpl_soup.find("img", class_="fancybox-image")["src"]

    featured_image_url = jpl_base_url + featured_image_url

    return featured_image_url

def scrape_mars_facts():
    # Visit the Mars Facts webpage [here](https://space-facts.com/mars/) 
    mars_facts_url = 'https://space-facts.com/mars/'

    # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    tables = pd.read_html(mars_facts_url)

    #grab the second table
    mars_facts_df = tables[1]
    mars_facts_html = mars_facts_df.to_html(header=False, classes='table')

    return mars_facts_html

def scrape_mars_hemi_img():
    browser = init_browser()

    base_usgs_url = 'https://astrogeology.usgs.gov'
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    browser.visit(usgs_url)

    time.sleep(5)

    html = browser.html
    usgs_html = BeautifulSoup(html, 'html.parser')

    hemi_image_urls = usgs_html.find_all('div', class_='description')

    mars_hemi_stuff = []

    for i in hemi_image_urls:
        hemi_img_url = base_usgs_url + i.a['href']
        browser.visit(hemi_img_url)
        time.sleep(5)
        
        html = browser.html
        hemi_html = BeautifulSoup(html, 'html.parser')
        
        hemi_title = hemi_html.find("title").text
        hemi_full_img_url = base_usgs_url + hemi_html.find("img", class_="wide-image")["src"]
        
        mars_hemi_stuff.append({'title': hemi_title, 'img_url': hemi_full_img_url})

    return mars_hemi_stuff