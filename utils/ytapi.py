import json
import urllib.request
import string
import random

count = 1
API_KEY = 'AIzaSyCC4X40Bx7oju-xftdKm9qPXnqfp6IY7dk'
random = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY, count, random)
webURL = urllib.request.urlopen(urlData)
data = webURL.read()
encoding = webURL.info().get_content_charset('utf-8')
results = json.loads(data.decode(encoding))

for data in results['items']:
    videoId = (data['id']['videoId'])
    print("https://youtu.be/" + videoId)
