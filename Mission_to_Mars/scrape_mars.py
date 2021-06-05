import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import datetime
import requests 

def scrape():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    client.drop_database('mars_db')
    db = client.mars_db
    collection = db.articles

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_dict = {'article_title':[], 'article_date':[], 'article_paragraph':[],
                'featured_image_url':[]}

    results =soup.find('div', class_='grid_layout')
    list_1 = results.find('li', class_='slide')
    container = list_1.find('div', class_='image_and_description_container')
    container_text = container.find('div', class_='list_text')

    mars_title = container_text.find('a').text
    mars_p = container.find('div', class_='article_teaser_body').text
    mars_date = container_text.find('div', class_='list_date').text
    mars_dict['article_title'].append(mars_title)
    mars_dict['article_date'].append(mars_date)
    mars_dict['article_paragraph'].append(mars_p)

    image_url ='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(image_url)
    base_url='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('div', class_='header')
    link = results.find('img', class_='headerimage')['src']
    featured_mars_url = f'{base_url + link}'
    mars_dict['featured_image_url'].append(featured_mars_url)

    url = 'https://space-facts.com/mars/'
    mars_fact_tabe = pd.read_html(url)
    mars_table=mars_fact_tabe[0]
    mars_fact = mars_table.to_html()
    mars_dict['mars_facts'] = mars_fact

    mars_hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemis_url)
    base_url ='https://astrogeology.usgs.gov'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results =soup.find_all('div', class_='description')
    hemi_dict={'hemi_title':[], 'img_url':[]}
    for names in results:
        hemi = names.find('h3').text
        browser.click_link_by_partial_text(hemi)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        mars_img_url = soup.find_all('img')[5]['src']
        hemi_dict['hemi_title'].append(hemi)
        hemi_dict['img_url'].append(base_url + mars_img_url)
        browser.back()
    mars_dict['title'] = hemi_dict
    browser.quit()
   

    return mars_dict