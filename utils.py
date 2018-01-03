import urllib.request as urllib2


def url_resolver(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = urllib2.Request(url)
    res = opener.open(response)
    return [res, res.geturl()]

def trim(name):
    return name.strip('\n').lower()



