from urllib.parse import urlparse


# Get domain name (example.com)
def get_domain_name(url):
    try:
        if "mobile.nytime" in url:
            return ''
        results = get_sub_domain_name(url).split('/')
        tmp = results[0].split('.')
        i = -1
        for element in results:
            i += 1
            if element == 'world':
                break
        return tmp[-2] + '.' + tmp[-1] + '/' +results[i]
    except:
        return ''


# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc + urlparse(url).path
    except:
        return ''


