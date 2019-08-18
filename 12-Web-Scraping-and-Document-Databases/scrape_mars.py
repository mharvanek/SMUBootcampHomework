from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd

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
    mars_news = scrape_mars_news
    return mars_news


def scrape_mars_news():

    mars_news = []

    # URL of page to be scraped
    mars_news_url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    mars_news_response = requests.get(mars_news_url)
    # Create BeautifulSoup object; parse with 'lxml'
    mars_news_html = BeautifulSoup(mars_news_response.text, 'lxml')

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