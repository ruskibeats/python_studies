
import requests
import lxml.html
from lxml import etree
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
}
pagetoLoad = 'http://www.google.com/search?q=site:linkedin.com/company \"@rainmaker.solutions\" OR \"rainmaker.solutions\" OR \"Rainmaker Solutions uk\"&num=1'
html = requests.get(headers=headers, pagetoLoad)


# html = requests.get(
# headers=headers,
# url='http://www.google.com/search?q=site:linkedin.com/company \"@rainmaker.solutions\" OR \"rainmaker.solutions\" OR \"Rainmaker Solutions uk\"'
text = html.content
doc = lxml.html.fromstring(text)
results = doc.xpath('.//h3[@class="LC20lb DKV0Md"]/text()')
print (results)
