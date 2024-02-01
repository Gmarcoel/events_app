from extract.scrapers.web_scraper import WebScraper
import requests
from bs4 import BeautifulSoup
from models.event import Event
from selenium.webdriver.chrome.options import Options
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

class CivitatisScraper(WebScraper):
    """
    A class for scraping the Civitatis website.
    """

    def __init__(self, base_url, target_urls):
        self.base_url = base_url
        self.target_urls = target_urls
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")                    
        self.chrome_options.add_argument("--disable-dev-shm-usage") 
        self.chrome_options.add_argument("--headless")
        self.activities_urls = []

    def get_data(self):
        """
        Gets data from the Atrapalo website.
        Returns:
                List[Dict[str, Any]]: A list of dictionaries containing the data.
        """
        for category in self.target_urls:
            url = self.target_urls[category]

            # 1. Get the URLs for all pages
            self.get_event_pages_urls(self.base_url+url)

            # 2. For each page, get all the event titles and URLs
            activities_links_dict = {}
            for page_url in self.activities_urls:
                page_events_dict = self.__scrape_page(page_url)
                activities_links_dict.update(page_events_dict)

            # 3. For each event in the dict, get the data
            activities_data = []
            for index, (title, url) in enumerate(activities_links_dict.items()):
                print(f"Scraping activity: {title}")
                event = self.__scrape_event(url)
                if not event:
                    continue
                event.categories = category
                event.portrait = None
                activities_data.append(event)
                if index > 1:
                    break

        return activities_data

    def get_event_pages_urls(self, target_url):
        """

        :return:
        """
        self.activities_urls.append(target_url)
        response = requests.get(target_url)
        soup_activities = BeautifulSoup(response.content, 'html.parser')
        pages_url = self.__get_pages_urls(soup_activities)
        self.activities_urls.extend(pages_url)


    def __scrape_page(self, url):
        """
        Scrape one page and get the event title and event URL for all events in the page

        :return:
            Dict[str, str]: A dictionary containing the event title and event URL
        """
        page_activities = {}

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        activity_links = soup.find_all('a', class_='_activity-link')
        activity_names = soup.find_all('h3', class_='comfort-card__title')

        for activity in activity_links:
            page_activities[activity_names[activity_links.index(activity)].text] = activity['href']

        return page_activities

    def __get_pages_urls(self, soup):
        pages_url = []

        pagination_nav = soup.find('div', class_='o-pagination__center')
        pages = pagination_nav.find_all('a')

        for page in pages:
            pages_url.append(page['href'])

        return pages_url

    def __scrape_event(self, url):
        response = requests.get(self.base_url + url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # TITLE
        if soup.find('h1', class_='a-title-activity') is None:
            title = 'N/D'
        else:
            title = soup.find('h1', class_='a-title-activity').text

        # DESCRIPTION
        if soup.find('div', id='descripcion') is None:
            description = 'N/D'
            return None
        else:
            div_desc_prev = soup.find('div', id='descripcion')
            description_text = div_desc_prev.get_text(strip=True)
            description = description_text

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        print(self.base_url + url)
        driver.get(self.base_url + url)
        sleep(2)

        # PRICE
        try:
            div_precios = driver.find_element(By.CSS_SELECTOR, "#precios")
        except Exception:
            div_precios = None

        if div_precios is not None:
            precios = div_precios.find_elements(By.CLASS_NAME, "component_priceActivity-price-rate")
            if precios is not None:
                # check if precios is a list
                if len(precios) > 1:
                    prices = precios[0].text
                else:
                    prices = 'N/D'            

        # ADDRESS
        div_address = soup.find('div', class_='directions')
        if div_address is None:
            address = 'N/D'
        else:
            address = div_address.find('p').text

        # COORDINATES
        # get data-markers attribute from div with id="meeting-point-map-container"
        div_map = soup.find('div', id='meeting-point-map-container')
        if div_map is not None:
            coords = div_map['data-markers']
            data = json.loads(coords)
            coordinates = data[0]
            lat = coordinates['lat']
            lon = coordinates['lng']
            coords = (lat, lon)
        else:
            coords = ('N/D', 'N/D')

        # DATE
        date = driver.find_element(By.CSS_SELECTOR, ".m-activity-detail-description").text

        # CATEGORIES
        cat = 'Cultura'

        # LANGUAGE
        if soup.find('h3', class_='_language') is None:
            lan = 'N/D'
        else:
            h3_lan = soup.find('h3', class_='_language')
            lan = h3_lan.find_next_sibling('p').text

        # DATA/MISCELLANEOUS
        data = {}
        main_info = driver.find_elements(By.CSS_SELECTOR, "#detalles")
        if main_info is not None:
            # get all elements with class="m-activity-detail"
            details = main_info[0].find_elements(By.CLASS_NAME, "m-activity-detail")
            for detail in details:
                # get element with class="m-activity-detail"
                detail_title = detail.find_element(By.CLASS_NAME, "a-title--activity-detail").text
                # get all text from p elements
                p_list = detail.find_elements(By.TAG_NAME, "p")
                text = ''
                for p in p_list:
                    text += p.text + '\n'

                if detail_title != 'Preguntas frecuentes':
                    data[detail_title] = text

            
        # IMAGES
        images = []
        div_images = soup.find('div', id='slide-container')
        if div_images is not None:
            images_list = div_images.find_all('img')
            for image in images_list:
                if image['src'].startswith('/f'):
                    images.append('https://www.civitatis.com'+image['src'])
                elif image['data-src'].startswith('/f'):
                    images.append('https://www.civitatis.com'+image['data-src'])

            # PORTRAIT
            print(images)            
            portrait = images[0] if len(images) > 0 else None
            print('portrait', portrait)
        
        # COMMENTS
        comments = []
        div_comments = soup.find_all('div', itemprop='review')
        if div_comments is not None:
            for div_comment in div_comments:
                # get p element with class="a-opinion"
                comment_description = div_comment.find('p', class_='a-opinion')
                comment_name = div_comment.find('p', class_='opi-name').text
                comment_rating = div_comment.find('span', class_='m-rating-stars')['title'].split(':')[1]
                comments.append(
                    {'user': comment_name, 
                     'description': comment_description.text, 
                     'rating': comment_rating})

        ev = Event(title, description, prices, address, date, cat, coords[0], coords[1], 
                   lan, portrait, images, data, comments)
        
        return ev
    
    def __to_event(self, data):
        """
        Converts the data to an Event object.
        :param data:
        :return:
        """
        return Event(data['title'], data['description'], data['price'], data['address'], data['date'], data['category'],
                     data['latitude'], data['longitude'], data['language'])



