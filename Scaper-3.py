import requests
import lxml.html
import csv

try:
    with open('1.html') as fi:
        text = fi.read()
except:
    html = requests.get('https://www.thomsonlocal.com/search/london/london?page=3')
    text = html.content

with open('1.html', 'wb') as fo:
    fo.write(text)

doc = lxml.html.fromstring(text)
# Another tip, name your variables like business_details (snake case) or businessDetails (camel case),
# I noticed you named your variables like business_Details, this is something looked down upon by
# the coding community. But since it is a personal project, it really shouldn't matter. However,
# if you are contributing to someone else's code it is important to keep this in mind. Therefore,
# better to develop a habit to use universally accepted variable names :)
businessDetails = []
# Obtain each li element(posting) individually
results = doc.xpath('//ol[@class="resultsBlock"]/li')
# Iterate through each posting
for result in results:
    # Here you could do result.xpath(...)[0], however this would raise an error
    # in the case there is no match (as it would return an empty list - [])
    # Returns a list [businessName] or [] if no match is found
    businessName = result.xpath('.//h2[@itemprop="name"]/text()')
    streetAddress = result.xpath('.//span[@itemprop="streetAddress"]/text()')  # Similar as above
    addressLocality = result.xpath(
        './/span[@itemprop="addressLocality"]/text()')  # Similar as above
    postalCode = result.xpath('.//span[@itemprop="postalCode"]/text()')  # Similar as above
    webSite = result.xpath('.//a[@itemprop="sameAs"]/@href')  # Similar as above
    businessDetail = [businessName, streetAddress, addressLocality, postalCode, webSite]
    print (businessDetail)

# Checks for which attribute is missing, this eliminates the
# need to error check each each variable
    for i in range(len(businessDetail)):
        # Check if entry is present
        if len(businessDetail[i]) > 0:
            businessDetail[i] = businessDetail[i][0]
# If entry
            print (businessDetail[i][0])
        else:
            print ('There is a missing attribute')
            print (businessDetail[i])
            businessDetail[i] = ''
    print (businessDetail[i])
    businessDetails.append(businessDetail)

    print (businessDetails)
f = open('/Users/russellbatchelor/Dropbox/pythonwork/thomsonlocal.csv', 'a')

writer = csv.writer(f)
writer.writerow(['Name', 'Address', 'Location', 'Postcode', 'Website'])
print (businessDetail)
# Write out each result obtained individually
for businessDetail in businessDetails:

    writer.writerow(businessDetail)
