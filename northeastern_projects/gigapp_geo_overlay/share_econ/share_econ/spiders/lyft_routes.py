import scrapy
import googlemaps
import pandas as pd 
from bs4 import BeautifulSoup
import requests
import json
import re
import traceback
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

class LyftRoutesSpider(scrapy.Spider):
    name='lyft_routes'
    base_url = 'https://maps.googleapis.com/maps/api/directions/json?'

    def __init__(self, locale=None, *args,**kwargs):
        super(LyftRoutesSpider, self).__init__(*args, **kwargs)
        self.locale = locale

    def get_api_key(self):
        json_file = open('gcp_key.json')
        json_obj = json.load(json_file)
        gcp_key = json_obj['key']
        return gcp_key

    def get_route_pairs(self):
        df = pd.read_csv(f'{self.locale}_route_export.csv')
        origins = df.origin_string.values
        destinations = df.destination_string.values
        return list(zip(origins, destinations))

    def clean_orig_dest_str(self, x, locale):
        if locale is not None:
            cleaned_str = x + f'+{locale}'
        else:
            cleaned_str = x
        pattern = re.compile(r'([a-zA-Z\+]{1,}\d{1,}[a-zA-Z\+]{1,})|([a-zA-Z\+]{1,}\d{1,}[a-zA-Z\+]{1,}\+\d{1,})|([a-zA-Z\+]{1,}\+\d{1,})|([a-zA-Z\+]{1,})')
        result = pattern.search(x).group(0)
        if result is not None:
            cleaned_str = result + f'+{locale}'
            print(f'{x} was changed to {cleaned_str}')
        return cleaned_str

    def start_requests(self):
        api_key = self.get_api_key()
        pairs = self.get_route_pairs()
        for pair in pairs:
            print(pair[0], pair[1])
            request_url = self.base_url + 'origin=' + self.clean_orig_dest_str(pair[0], self.locale) + '&destination=' + self.clean_orig_dest_str(pair[1], self.locale) + '&key=' + api_key
            # print(request_url)
            yield scrapy.Request(url=request_url, callback=self.geocode_routes)

    def geocode_routes(self, response):
        try:
            url = response.url
            print('-'*100)
            print('Begin geocoding data on route response from Google Directions API for: %s', url)
            print('-'*100)

            json_response = json.loads(response.body_as_unicode())
            pp.pprint(json_response)
            print('-'*100)

            for route in json_response['routes']:
                if route is not None:
                    print('Google API found a route with the provided origin/destination pair')
                    item = {}
                    item['start_address'] = route['legs'][0]['start_address']
                    item['end_address'] = route['legs'][0]['end_address']
                    item['start_coords'] = (route['legs'][0]['start_location']['lat'], route['legs'][0]['start_location']['lng'])
                    item['end_coords'] = (route['legs'][0]['end_location']['lat'], route['legs'][0]['end_location']['lng'])
                    item['total_distance'] = float(route['legs'][0]['distance']['text'].split(' ')[0])
                    item['unit_distance'] = route['legs'][0]['distance']['text'].split(' ')[1]
                    step_list = []
                    steps = route['legs'][0]['steps']
                    for i in range(len(steps)):
                        step_list.append((steps[i]['start_location']['lat'], steps[i]['start_location']['lng']))
                        if i == len(steps) - 1:
                            step_list.append((steps[i]['end_location']['lat'], steps[i]['end_location']['lng']))
                    item['step_list'] = step_list
                    yield item
                else:
                    print('Google API did not find any routes with provided origin/destination pair')
                    yield {}
        except Exception as e:
            print('-'*80)
            print("Exception in article parsing code block: %s", e)
            traceback.print_exc(file=sys.stdout)
            print('-'*80)
        