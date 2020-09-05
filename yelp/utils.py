from urllib.parse import urlencode


locations = ['Iowa']
description= 'Plumbers'

def get_urls():
    url_list=[]
    for location in locations:
        props= {'find_desc':description, 'find_loc':location, 'ns':'1'}
        url = 'https://yelp.co.uk/search?' + urlencode(props)
        url_list.append(url)
    return url_list
