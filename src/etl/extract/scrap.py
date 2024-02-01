from extract.scrapers.atrapalo_scraper import AtrapaloScraper
from extract.scrapers.civitatis_scraper import CivitatisScraper

def scrape_activities():
    webs = {

        'Civitatis':
        {
            'base_url': 'https://www.civitatis.com',
            'target_urls': {
                'Cultura': '/es/madrid/'
            },
            'scraper': CivitatisScraper
        },
        'Atrapalo':
        {
            'base_url': 'https://www.atrapalo.com',
            'target_urls':
                {
                    'Deportes': '/actividades/madrid/deportes-y-aventuras/',
                    'Cultura': '/actividades/madrid/cultura',
                    'Gastronomia': '/actividades/madrid/gastronomia',
                    'Bienestar': '/actividades/madrid/bienestar/'
                },
            'scraper': AtrapaloScraper
        },
    }

    data = []
    for web in webs:
        # if scraper then scrap
        if 'scraper' in webs[web]:
            data += webs[web]['scraper'](webs[web]['base_url'], webs[web]['target_urls']).get_data()            
        else:
            print('no scraper', webs[web])
    

    return data

if __name__ == '__main__':
    scrape_activities()
