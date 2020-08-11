import requests
import lxml.html
import csv
import urllib2
import socket
import httplib
import re
from lxml import cssselect, html
import time
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
}
# Setup
pageCount = 0
totalPages = 0
businessDetails = []


def check_url(url, timeout=5):
    try:
        return urllib2.urlopen(url, timeout=timeout).getcode() == 200
    except urllib2.URLError as e:
        return False
    except socket.timeout as e:
        print False
    except httplib.HTTPException as e:
        print False
    except Exception:
        import traceback


# This website has more than 1 page so I need to iterate through
# I setup a loop based on the page count which I calculate through number of
# results divided by 25 which is the total number diplayed
while pageCount <= totalPages:
    pageCount = str(pageCount)
    # I open the URL for the first pass
    pagetoLoad = 'https://www.thomsonlocal.com/search/computer-support/wendover-buckinghamshire?sorting=reviews&page=' + pageCount
    html = requests.get(pagetoLoad)
    text = html.content
    doc = lxml.html.fromstring(text)
    print (pagetoLoad)
    # Some quick maths for the number of iterations I will need to do
    results = doc.xpath('//ol[@class="resultsBlock"]/li')
    totalResults = doc.xpath('.//span[@class="totalResults"]/text()')
    # I convert a list to a string
    totalResults = str(totalResults)
    # Strip out everything but the digits and convert the result to an integer
    totalResults = int(totalResults.replace("['", "").replace("Results found']", ""))
    # I work in the negative to make the roundup maths easier
    totalPages = (-(-totalResults/25))

    # Iterate through each posting
    for result in results:

        # Here you could do result.xpath(...)[0], however this would raise an error
        # in the case there is no match (as it would return an empty list - [])
        # Returns a list [businessName] or [] if no match is found
        businessName = result.xpath('.//h2[@itemprop="name"]/text()')
        streetAddress = result.xpath(
            './/span[@itemprop="streetAddress"]/text()')  # Similar as above
        addressLocality = result.xpath(
            './/span[@itemprop="addressLocality"]/text()')  # Similar as above
        postalCode = result.xpath('.//span[@itemprop="postalCode"]/text()')  # Similar as above
        webSite = result.xpath('.//a[@itemprop="sameAs"]/@href')  # Similar as above
        webResult = str(webSite).strip('[]').strip("'")
        webCheck = str(check_url(webResult))
        businessDetail = [businessName, streetAddress,
                          addressLocality, postalCode, webSite, webCheck]
        # We are going to search Linkedin for a single profile
        # the search string is built from a web address and email address plus
        # some more detail made from the businessName
        # we only want one result

        urlMain = 'site:linkedin.com/company '
        wwwString = str(webSite)
        busString = str(businessName)
        searchEmail = (re.sub(r'http:\/\/www.', '@', wwwString)[1:-1])
        searchDomain = (re.sub(r'http:\/\/www.', '', wwwString)[1:-1])
        # searchDetail = str(busString + " ")[1:-1]
        oR = ' OR '

        builtUrl = urlMain+searchEmail+oR+searchDomain
        params = {
            'access_key': '7a0cc694ec52a284c7e8cfd6e4e7116e',
            'query': builtUrl
        }

        if webCheck == 'True':
            #print ('hello')
            #print params
            api_result = requests.get('http://api.serpstack.com/search', params)
            api_response = api_result.json()
            googleResults = api_response['organic_results']
            if len(googleResults) > 0:
                #print ('googleResults', googleResults)
                linkeDin = googleResults[0]['url']
                #print ('googleCheck', googleCheck)
            else:
                linkeDin = ['']
        else:
            linkeDin = ['']
        businessDetail.append([linkeDin])

    # Checks for which attribute is missing, this eliminates the
    # need to error check each each variable
        for i in range(len(businessDetail)):
            # Check if entry is present
            if len(businessDetail[i]) > 0:
                businessDetail[i] = businessDetail[i][0]
            else:
                businessDetail[i] = ''
        businessDetails.append(businessDetail)
    f = open('/Users/russellbatchelor/Dropbox/pythonwork/thomsonlocal.csv', 'w')

    writer = csv.writer(f)
    writer.writerow(['Name', 'Address', 'Location', 'Postcode',
                     'Website', 'Website', 'googleCheck'])
    # Write out each result obtained individually
    for businessDetail in businessDetails:
        writer.writerow(businessDetail)
    # I convert pagecount to integer to update the counter, pageCount is used to
    # to construct the URL - there is probably a better way of doing this
    pageCount = int(pageCount)
    pageCount = pageCount + 1
# I close the file after I have iterated through all pages
f.close()
print ('end')
