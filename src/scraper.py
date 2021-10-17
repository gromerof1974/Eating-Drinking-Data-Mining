'''
-------------------------------------------------------------------------------------------------------
Scraper to get data info from the restaurants of a city
-------------------------------------------------------------------------------------------------------    
''' 

import json 
import requests
import time
from numpy import random
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

'''
-------------------------------------------------------------------------------------------------------
scrape 
-------------------------------------------------------------------------------------------------------    
'''
def scrape(city, debug_enabled, scroll_down):
    start_time = time.time()

    links_dictionary = get_links(city, debug_enabled, scroll_down)
    print_dictionary(links_dictionary, debug_enabled)
    dic = {}
    i = 1
    len_links_dictionary = len(links_dictionary)
    for key in links_dictionary:
        print('Processing', i, 'of', len_links_dictionary)
        dic.update(get_page_data(city, key, links_dictionary[key], debug_enabled))
        i += 1
 
    save_dictionary_to_file(dic, city.replace(' ', '_') + '_restaurants.csv', debug_enabled)

    elapsed_time = time.time() - start_time
    print('Total elapsed time ',  time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), '\n')


'''
-------------------------------------------------------------------------------------------------------
Return dictionary where:
key = name of restaurant
value = url of restaurant
-------------------------------------------------------------------------------------------------------    
'''        
def get_links(city, debug_enabled, scroll_down):
    links_dictionary = {}
    
    referer = 'https://es.restaurantguru.com/' 
    url = referer + city.lower().replace(' ', '-')
    if (scroll_down):
        show_browser = False    
        html = scroll_down_to_bottom(url, show_browser, debug_enabled)
        soup = BeautifulSoup(html, features='html.parser')
    else:    
        page = requests.get(url, headers = get_headers(referer))
        soup = BeautifulSoup(page.content, features='html.parser')
        if page.status_code != 200:
            print('The page could not be retrieved', url)
            return links_dictionary
        
    lista_tag_a = soup.findAll('a', {'class': 'notranslate title_url'})
    for tag_a in lista_tag_a:
        links_dictionary.update({tag_a['title'] : tag_a['href']})
    return links_dictionary   


'''
-------------------------------------------------------------------------------------------------------
Returns the page source after scrolling to the end using Selenium library
-------------------------------------------------------------------------------------------------------    
''' 
def scroll_down_to_bottom(url, show_browser, debug_enabled):
    SCROLL_PAUSE_TIME = 2.0

    print('Init Selenium scroll down to bottom (this operation may take several seconds)...') 
    driver = get_chrome_driver(show_browser)
    driver.get(url);
    
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        if (debug_enabled):
            print('Still scrolling...')
            
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height    
    
    html = driver.page_source
    
    driver.quit()
    print('End Selenium scroll down to bottom')
    
    return html

    
'''
-------------------------------------------------------------------------------------------------------
Return Chrome driver to interact with the web page
-------------------------------------------------------------------------------------------------------    
''' 
def get_chrome_driver(show_browser):
    if (show_browser):
        driver = webdriver.Chrome('./chromedriver.exe')
    else:
        op = webdriver.ChromeOptions()
        op.add_argument('--headless')
        driver = webdriver.Chrome('./chromedriver.exe', options=op)
    return driver   

    
'''
-------------------------------------------------------------------------------------------------------
Sleep a random number of seconds between 1 and 2
-------------------------------------------------------------------------------------------------------    
'''    
def sleep_random(debug_enabled):
    sleep_time = random.uniform(1, 2)
    if (debug_enabled):
        print('Sleep for ', sleep_time, 'seconds')
    sleep(sleep_time)
    if (debug_enabled):
        print('Sleep end')     
          

'''
-------------------------------------------------------------------------------------------------------
Return request header (obtained from the browser with Chrome Developer Tools) 
-------------------------------------------------------------------------------------------------------    
''' 
def get_headers(referer):
    headers = {'Referer' : referer,
               'sec-ch-ua' : '\"Chromium\";v="94", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"',
               'sec-ch-ua-mobile' : '?0',
               'sec-ch-ua-platform' : '\"Windows\"',
               'Upgrade-Insecure-Requests' : '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    
    return headers   


'''
-------------------------------------------------------------------------------------------------------
Get page data 
-------------------------------------------------------------------------------------------------------    
''' 
def get_page_data(city, page_name, url, debug_enabled):
    dic = {}
    
    start_time = time.time()

    sleep_random(debug_enabled)

    if (debug_enabled):
        print('Processing [', page_name, ']: ', url)


    referer = 'https://es.restaurantguru.com/' + city.lower().replace(' ', '-') 
    
    page = requests.get(url, headers = get_headers(referer))
    soup = BeautifulSoup(page.content, features='html.parser')

    avg_price = get_average_price(soup)
    cuisine_features = get_cuisine_features(soup)
    telephone = get_telephone(soup)
    address = get_address(soup)
    location = get_location(soup)
    opinions = get_opinions(soup)
    ratings = get_ratings(soup)
    comments_count = get_comments_count(soup)
    features = get_features(soup)
    schedule = get_schedule(soup)
    appetizing_dishes = get_appetizing_dishes(soup)
    restaurant_features = get_restaurant_features(soup)
    similar_restaurants = get_similar_restaurants(soup)
    web_site = get_web_site(soup)
    
    csv_line = list()
    csv_line.append(page_name)
    csv_line.append(avg_price)
    csv_line.append(cuisine_features) 
    csv_line.append(telephone) 
    csv_line.append(address)
    csv_line.append(location)
    csv_line.append(opinions)
    csv_line.append(ratings)
    csv_line.append(comments_count)
    csv_line.append(features)
    csv_line.append(schedule)
    csv_line.append(appetizing_dishes)
    csv_line.append(restaurant_features)
    csv_line.append(similar_restaurants)
    csv_line.append(web_site)    
    
    if (debug_enabled):
        print('\t', 'avg_price: ', avg_price)
        print('\t', 'cuisine_features: ', cuisine_features)
        print('\t', 'telephone: ', telephone)
        print('\t', 'address: ', address)
        print('\t', 'location: ', location)
        print('\t', 'opinions: ', opinions)
        print('\t', 'ratings: ', ratings)
        print('\t', 'comments_count: ', comments_count)
        print('\t', 'features: ', features)
        print('\t', 'schedule: ', schedule)
        print('\t', 'appetizing_dishes: ', appetizing_dishes)
        print('\t', 'restaurant_features: ', restaurant_features)
        print('\t', 'similar_restaurants: ', similar_restaurants)
        print('\t', 'web_site: ', web_site)
        
        elapsed_time = time.time() - start_time
        print('Processing [', page_name, ']: elapsed time ',  time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), '\n')
    
    dic.update({page_name : ';'.join(csv_line)})
    return dic  


def get_average_price(soup):
    tag_div = soup.find('div', {'class': 'short_info with_avg_price'})
    if (tag_div is None):
        return ''
    tag_span_text_overflow = tag_div.find('span', {'class': 'text_overflow'})
    return tag_span_text_overflow.text.strip().replace('\n', '')


def get_cuisine_features(soup):
    tag_div = soup.find('div', {'class': 'cuisine_wrapper'})
    if (tag_div is None):
        return ''
    return tag_div.text.strip().replace('\n', '')


def get_telephone(soup): 
    tag_a = soup.find('a', {'class': 'header_call'})
    if (tag_a is None):
        return ''
    return tag_a['href']


def get_address(soup): 
    tag_span = soup.find('span', {'class': 'header_address open-map'})
    if (tag_span is None):
        return ''
    return tag_span.text.strip().replace('\n', '').replace(';', ',')


def get_location(soup): 
    tag_div = soup.find('div', {'class': 'address', 'id' : 'info_location'})
    if (tag_div is None):
        return ''
    list_tag_div = tag_div.findAll('div')
    for tag_div in list_tag_div:
        if (tag_div.has_attr('class') == False):
                return tag_div.text.strip().replace('\n', '').replace(';', ',')
    return ''        


def get_opinions(soup):
    dic = {}
    list_tag_div = soup.findAll('div', {'class': 'f_meals'})
    for tag_div in list_tag_div:
        list_tag_a = tag_div.findAll('a', {'class': 'tag'})
        for tag_a in list_tag_a:
            dic.update({tag_a.text.strip().replace('\n', '') : tag_a['class'][1]})
    json_object = json.dumps(dic)        
    return json_object.replace('\n', '')
    

def get_ratings(soup):
    dic = {}
    list_tag_a = soup.findAll('a', {'class': 'rating_list_right'})
    for tag_a in list_tag_a:
        tag_p = tag_a.find('p')
        tag_div_no_rating = tag_a.find('div', {'class': 'no_rating'})
        if (tag_div_no_rating is None):

            tag_div_google_stars = tag_a.find('div', {'class': 'google_stars'})
            if tag_div_google_stars is not None:
                tag_div_fill = tag_div_google_stars.find('div', {'class': 'fill'})
                rating = tag_div_fill['style'].replace('width: ', '').replace('%;', '')
                dic.update({tag_p.text.strip().replace('\n', '') : str('{:.1f}'.format(int(rating)*5/100)) + '/5'})
            
            tag_div_trip_block = tag_a.find('div', {'class': 'trip_block'})
            if tag_div_trip_block is not None:
                tag_div_fill = tag_div_trip_block.find('div', {'class': 'fill'})
                tag_a_trip = tag_div_fill.find('a')
                rating = tag_a_trip['width']
                dic.update({tag_p.text.strip().replace('\n', '') : str('{:.1f}'.format(int(rating)*5/100)) + '/5'})

            tag_div_facebook_rate = tag_a.find('div', {'class': 'facebook_rate'})
            if tag_div_facebook_rate is not None:
                tag_span = tag_div_facebook_rate.find('span')
                dic.update({tag_p.text.strip().replace('\n', '') : tag_span.text.strip().replace('\n', '') + '/5'})
        else:
            dic.update({tag_p.text.strip().replace('\n', '') : tag_div_no_rating.text.strip().replace('\n', '')})    

    list_tag_div = soup.findAll('div', {'class': 'rating_list_right'})
    for tag_div in list_tag_div:
        tag_p = tag_div.find('p')
        tag_div_no_rating = tag_div.find('div', {'class': 'no_rating'})
        if (tag_div_no_rating is None):
            tag_div_trip_block = tag_div.find('div', {'class': 'trip_block'})
            if tag_div_trip_block is not None:
                tag_div_fill = tag_div_trip_block.find('div', {'class': 'fill'})
                tag_img = tag_div_fill.find('img')
                rating = tag_img['width']
                dic.update({tag_p.text.strip().replace('\n', '') : str('{:.1f}'.format(int(rating)*5/100)) + '/5'})
        else:
            dic.update({tag_p.text.strip().replace('\n', '') : tag_div_no_rating.text.strip().replace('\n', '')})    
    
    json_object = json.dumps(dic)        
    return json_object.replace('\n', '')    


def get_comments_count(soup):
    dic = {}
    list_tag_a = soup.findAll('a', {'class': 'rating_list_right'})
    for tag_a in list_tag_a:
        tag_p = tag_a.find('p')
        tag_span = tag_a.find('span', {'class': 'comments_count'})
        if (tag_span is None):
            dic.update({tag_p.text.strip().replace('\n', '') : 0})
        else:
            dic.update({tag_p.text.strip().replace('\n', '') : tag_span.text.strip().replace('\n', '')})
            
    list_tag_div = soup.findAll('div', {'class': 'rating_list_right'})
    for tag_div in list_tag_div:
        tag_p = tag_div.find('p')
        tag_span = tag_div.find('span', {'class': 'comments_count'})
        if (tag_span is None):
            dic.update({tag_p.text.strip().replace('\n', '') : 0})
        else:
            dic.update({tag_p.text.strip().replace('\n', '') : tag_span.text.strip().replace('\n', '')})
    
    json_object = json.dumps(dic)        
    return json_object.replace('\n', '')    
   

def get_features(soup):
    str_list = list() 
    tag_div_features_block = soup.find('div', {'class': 'features_block'})
    if (tag_div_features_block is None):
        return ''
    tag_div_overflow = tag_div_features_block.find('div', {'class': 'overflow'})
    list_tag_span = tag_div_overflow.findAll('span')
    for tag_span in list_tag_span:
        str_list.append(tag_span.text.strip().replace('\n', ''))
    return ', '.join(str_list)
    

def get_schedule(soup):
    dic = {}
    tag_table = soup.find('table', {'class': 'schedule-table'})
    if (tag_table is None):
        return ''
    list_tag_tr = tag_table.findAll('tr')
    for tag_tr in list_tag_tr:
        list_tag_td = tag_tr.findAll('td')
        tag_span = list_tag_td[0].find('span', {'class': 'full-day'})
        list_td_contents = list_tag_td[1].contents
        value = ''
        for td_content in list_td_contents:
            if (len(td_content) > 0):
                if (len(value) > 0):
                    value += ', '
                value += td_content    

        dic.update({tag_span.text.strip().replace('\n', '') : value})
    
    json_object = json.dumps(dic)        
    return json_object.replace('\n', '')      


def get_appetizing_dishes(soup):
    str_list = list() 
    tag_div_dishes = soup.find('div', {'class': 'tags_block dishes'})
    if (tag_div_dishes is None):
        return ''
    list_li = tag_div_dishes.findAll('li', {'class': 'o_meal'})
    for tag_li in list_li:
        str_list.append(tag_li.text.strip().replace('\n', ''))
    return ', '.join(str_list)
    

def get_restaurant_features(soup):
    str_list = list() 
    list_tag_div = soup.findAll('div', {'class': 'tags_block dishes'})
    i = 1
    for tag_div in list_tag_div:
        if (i == 1):
            i += 1
            continue # skip first tags_block dishes, corresponding to appetizing dishes 
        list_li = tag_div.findAll('li', {'class': 'o_meal'})
        for tag_li in list_li:
            str_list.append(tag_li.text.strip().replace('\n', ''))
        return ', '.join(str_list)
    return ''


def get_similar_restaurants(soup):
    str_list = list() 
    tag_div_similar = soup.find('div', {'class': 'wrapper_similar'})
    if (tag_div_similar is None):
        return ''
    list_tag_div = tag_div_similar.findAll('div', {'class': 'rest_title red'})
    for tag_div in list_tag_div:
        str_list.append(tag_div.text.strip().replace('\n', ''))
    return ', '.join(str_list)


def get_web_site(soup): 
    tag_div = soup.find('div', {'class': 'website'})
    if (tag_div is None):
        return ''
    list_tag_div = tag_div.findAll('div')
    for tag_div in list_tag_div:
        if (tag_div.has_attr('class') == False):
                return tag_div.text.strip().replace('\n', '')
    return ''   


'''
-------------------------------------------------------------------------------------------------------
Print dictionary if bool_debug = True
-------------------------------------------------------------------------------------------------------    
''' 
def print_dictionary(dic, debug_enabled):
    if (debug_enabled == False):
        return
    i=1;        
    for key in dic: 
        print('[', i, '] , ', key, ': ', dic[key])
        i+=1;   

    print('\n') 
    
    
''' 
-------------------------------------------------------------------------------------------------------
Save dictionary to file
-------------------------------------------------------------------------------------------------------
'''
def save_dictionary_to_file(dic, file_name, debug_enabled):
    if (debug_enabled):
        print('Saving file ', file_name) 
    
    with open(file_name, 'w', encoding="utf-8") as f:
        f.write('name;avg_price;cuisine_features;telephone;address;location;opinions;ratings;comments_count;\
                 features;schedule;appetizing_dishes;restaurant_features;similar_restaurants;web_site\n')
        for key in dic.keys():
            f.write('%s\n' %(dic[key]))
    
    if (debug_enabled):
        print('File ', file_name, ' saved')           
    