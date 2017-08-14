from urllib import *
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
import urllib.request
import requests

def download(url, user_agent, num_retries = 5):
    print('Downloading: ', url)
    headers = {'User-Agent': user_agent}

    request = urllib.request.Request(url, headers=headers)
    try:
        html = urlopen(request).read()
    except urllib.error.URLError as e:

        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:             
                html = download(url, user_agent, num_retries-1)
        else:
            print('Download error:', e.reason)
    except:
        html = None
    return html
            