import requests
import json
import urllib2
import urllib
import httplib

#these two paras control listing result and amount for each post request
current_page = 1
records_paper_page = 50

url1 = 'https://api2.realtor.ca/Listing.svc/PropertySearch_Post'
params = {
    "CultureId": "1",
    "ApplicationId": "1",
    "RecordsPerPage": "50",
    "MaximumResults": "9",
    "PropertySearchTypeId": "1",
    "PriceMin": "500000",
    "PriceMax": "1000000",
    "TransactionTypeId": "2",
    "StoreyRange": "2-0",
    "OwnershipTypeGroupId": "1",
    "BuildingTypeId": "1",
    "ConstructionStyleId": "3",
    "BedRange": "3-0",
    "BathRange": "2-0",
    "LongitudeMin": "-123.49159395683358",
    "LongitudeMax": "-121.62941133964608",
    "LatitudeMin": "48.45953616376967",
    "LatitudeMax": "49.821417271829674",
    "SortOrder": "A",
    "SortBy": "1",
    "OpenHouse": "1",
    "OpenHouseStartDate": "08/14/2016",
    "OpenHouseEndDate": "08/26/2016",
    "viewState": "l",
    "Longitude": "-122.64174005377839",
    "Latitude": "49.14514549678261",
    "ZoomLevel": "11",
    "CurrentPage": "1",
    "PropertyTypeGroupID": "1"
}
# Adding header
headers1 = {

'Host': 'api2.realtor.ca',
'Accept': '*/*',
'Content-Length': '586',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}


# cookie = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}
# req = urllib2.Request(url1)
# req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
# response = urllib2.urlopen(req,json.dumps(payload))
# r = urllib2.urlopen(url1, data=urllib.urlencode(payload)).read()
r = requests.post(url=url1,data=params,headers=headers1)
print r.content

print type(r.content)
result = json.loads(r.content)
result =  result['Results']
# print type(result)
print len(result)
f = open("result.txt","a+")
for item in result:
    for key,value in item.iteritems():
        # if key == "Id":
        #     print str(key) + ":" + str(value)
        f.writelines(str(key) + ":" + str(value))
f.close()