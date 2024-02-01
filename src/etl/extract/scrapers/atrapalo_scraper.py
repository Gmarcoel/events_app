from extract.scrapers.web_scraper import WebScraper
import requests
from bs4 import BeautifulSoup
from models.event import Event
from urllib.parse import urlparse, parse_qs, unquote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.options import Options

class AtrapaloScraper(WebScraper):
    """
    A class for scraping the Atrapalo website.
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

        1) Get name and URLs for all events of the given page
        2) For each event, get the data

        
        Returns:
                List[Dict[str, Any]]: A list of dictionaries containing the data.
        """
        # LOOP THROUGH ALL TARGET URLS
        activities_data = []
        for category in self.target_urls:
            url =self.target_urls[category]
            
            # 1. Get the URLs for all pages
            self.get_event_pages_urls(self.base_url+url)

            # 2. For each page, get all the event titles and URLs
            activities_links_dict = {}
            for page_url in self.activities_urls:
                page_events_dict = self.__scrape_page(page_url)
                activities_links_dict.update(page_events_dict)

            # 3. For each event in the dict, get the data
            for index, (title, (url, image)) in enumerate(activities_links_dict.items()):
                print(f"Scraping activity: {title}")
                event = self.__scrape_event(url)
                if not event:
                    continue
                event.categories = category
                event.portrait = self.base_url + image
                activities_data.append(event)
                if index > 2:
                    break
 
        return activities_data

    def get_event_pages_urls(self, target_url):
        """
        Gets the URLs of the events. For each page get the its URL
        Returns:
                Dict[str, str]: A dictionary containing the event title and event URL
        """

        # ACTIVIDADES
        self.activities_urls = []
        self.activities_urls.append(target_url)
        response = requests.get(target_url)
        soup_activities = BeautifulSoup(response.content, 'html.parser')

        while self.__has_new_page(soup_activities) is not None:
            next_page_url = self.__has_new_page(soup_activities)
            self.activities_urls.append(self.base_url + next_page_url)
            response = requests.get(self.base_url + next_page_url)
            soup_activities = BeautifulSoup(response.content, 'html.parser')

        print(f"Found {len(self.activities_urls)} pages of activities.")

    def __scrape_page(self, url):
        """
        Scrape one page and get the event title and event URL for all events in the page

        :return:
            Dict[str, str]: A dictionary containing the event title and event URL
        """
        page_activities = {}

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # get activities
        activitiy_names = soup.find_all('h2', class_='nombre')

        # get image sources
        containers = soup.find_all('a', class_='img-slot')
        images_html = [container.find('img', class_='event-img') if container.find('img', class_='event-img') is not None else container.find('img', class_='cartel-img') for container in containers]

        # Clean the data
        if len(images_html) > len(activitiy_names):
            images = images_html[:len(activitiy_names)]
        elif len(images_html) < len(activitiy_names):
            activitiy_names = activitiy_names[:len(images_html)]



        # get the URLs
        for index, activity in enumerate(activitiy_names):
            a = activity.find('a')
            href = a['href']
            src = images_html[index]['data-original']
            page_activities[a['title']] = (href, src)
            



        return page_activities

    def __has_new_page(self, soup):
        """
        Checks if there is a new page in the pagination and returns its URL if exists.
        :param soup:
        :return:
        """
        pagination      = soup.find('ul', class_='pagination__numbers')
        current_page    = pagination.find('li', class_='active')
        next_page       = current_page.find_next_sibling('li')

        if next_page is None:
            return None
        next_page_url   = next_page.find('a')['href']

        return next_page_url

    def __scrape_event(self, url):
        try:
            response = requests.get(self.base_url + url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
        except:
            print("ERROR scraping event. Timeout.")
            return None

        # title
        if soup.find('h1') is None:
            title = 'N/D'
        else:
            title = soup.find('h1').text

        # description
        if soup.find('div', class_='ou-description__content') is None:
            description = 'N/D'
        else:
            description = soup.find('div', class_='ou-description__content').text

        # price
        if soup.find('span', class_='ou-price__from') is None:
            price = 'N/D'
        else:
            span_price = soup.find('span', class_='ou-price__to')
            price = span_price.find('div', class_='aui-money').text

        # address
        if soup.find('p', class_='ou-location-box__location') is None:
            address = 'N/D'
        else:
            p_address = soup.find('p', class_='ou-location-box__location')
            address = p_address.findChildren('span', recursive=False)[0]
            address.a.decompose()
            address = address.text

        # coordinates
        if soup.find('div', class_='ou-location-box__map') is None:
            coords = ('N/D', 'N/D')
        else:
            map_url = soup.find('div', class_='ou-location-box__map')
            map_url = map_url.find('a')['href']
            coords = self.__parse_url(map_url)

        # DATE
        if soup.find('div', class_='ou-main-mainProductInfo__wrapper') is None:
            date = 'N/D'
        else:
            cont = soup.find('div', class_='ou-main-mainProductInfo__wrapper')
            date_cont = cont.findChildren('dd')[0]
            date = date_cont.text

        # portrait source
        portrait = None

        # IMAGES (with selenium)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        driver.get(self.base_url + url)
        sleep(2)
        
        carousel_items = driver.find_elements(By.CSS_SELECTOR, '.ou-item__wrapper')

        images = []
        
        for item in carousel_items:
            img = item.find_element(By.TAG_NAME, 'img')
            src = img.get_attribute('src')
            images.append(src)

        driver.quit()
            
        # categories
        cat = ""

        # language
        lan_span = soup.find('span', string='Idiomas')
        if lan_span is None:
            lan = 'N/D'
        else:
            lan_dl = lan_span.find_parent('dl')
            lan_dd = lan_dl.findChildren('dd')[0]
            lan = lan_dd.text
        
        # data
        data = {}
        main_info = soup.find('section', class_='ou-product-info')
        if main_info:
            # Obtener todos los dl dentro
            dls = main_info.find_all('dl', class_='ou-product-info-item')
            for dl in dls:
                # Obtener el dt de cada dl
                dt = dl.find('dt')
                # Obtener el titulo (span dentro de dt)
                data_title = dt.find('span').text
                # Obtener el texto (dd dentro de dl)
                dd = dl.find('dd')
                data_text = dd.text

                # Añadir al dict
                data[data_title] = data_text
        
        print(data)

        # Comments
        comments = []
        rws_results = soup.find('div', class_='rws-results')
        if rws_results:
            # sacar los li dentro del ul dentro del div
            lis = rws_results.find('ul').find_all('li')
            for li in lis:
                # find user inside li (including son and grandson, and ele)
                comment_user = li.find('p', class_='aui-avatar__title')
                if not comment_user:
                    continue
                comment_user = comment_user.text
                comment_description =  li.find('div', class_='rws-review-item-description').find('p')
                if not comment_description:
                    continue
                comment_description = comment_description.text
                comment_rating = li.find('div', class_='aui-rating-badge__value')
                if not comment_rating:
                    continue
                comment_rating = comment_rating.text
                comments.append({
                    'user': comment_user,
                    'description': comment_description,
                    'rating': comment_rating
                })


        # Save the info in a Event object and return as dict
        ev = Event(title, description, price, address, date, cat, coords[0], coords[1], lan, portrait, images, data, comments)
        return ev

    def __parse_url(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        encoded_coords = query_params.get('query', [None])[0]
        if encoded_coords:
            decoded_coords = unquote(encoded_coords)
            lat, lon = decoded_coords.split(',')
            return (lat, lon)
        else:
            print("Coordinates not found in URL.")

    def __to_event(self, data):
        """
        Converts the data to an Event object.
        :param data:
        :return:
        """
        return Event(data['title'], data['description'], data['price'], data['address'], data['date'], data['category'],
                     data['latitude'], data['longitude'], data['language'])