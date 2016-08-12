# encoding: utf-8

import scrapy


def write_file(file_name, data):
    with open(file_name, "a") as myfile:
        myfile.write(data)

import json

def write_json(file_name, data):
    with open(file_name, 'a') as outfile:
        json.dump(data, outfile)

def format_string(input_list):
    return ''.join(input_list).strip('\n')


def to_unicode(text):
    try:
        text = unicode(text, 'utf-8')
    except TypeError:
        return text

page_numbers_xpath = '//*[@id="numberOfPagedRecords"]'


house_selector = '//*[contains(@id, "m_map_map_prpty_lnk")]'

house_xpath = {'house_url':'//*[contains(@id, "result")]/a',
               'house_addr': '//*[contains(@id, "map_lst_address")]',
               'house_price':'//*[contains(@id, "map_lst_price")]',
               'house_mls_number':'//*[contains(@id, "map_lst_ID")]'
               }

from selenium import webdriver

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
url_driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')


def house_search(url, file_name):
    try:
        driver.get(url)
        import time
        time.sleep(30)

        page_info = driver.find_element_by_xpath(page_numbers_xpath).text
        house_counts = page_info.split(' ')[2]
        page_counts = int(int(house_counts) / 9) + 1

        print house_counts, page_counts
        houses = []
        for i in range(0, page_counts):
            house_urls = driver.find_elements_by_xpath(house_xpath['house_url'])

            for house in house_urls:
                house_url = house.get_attribute('href')
                print house_url
                url_driver.get(house_url)
                time.sleep(10)

                house_addr = url_driver.find_element_by_xpath('//*[@id="m_property_dtl_address"]').text
                house_price = url_driver.find_element_by_xpath('//*[@id="m_property_dtl_info_hdr_price"]').text
                house_mls_number = url_driver.find_element_by_xpath('//*[@id="FullPropertyDetailsContainer"]/div[1]/div[1]/div[1]/div[2]').text
                house_features = url_driver.find_element_by_xpath('//*[@id="divFeaures"]').text
                house_details = url_driver.find_element_by_xpath('//*[@id="rptBuildingDetails"]').text
                open_house_info = ''
                open_house_table = url_driver.find_elements_by_xpath('//*[@id="rptOpenHouse"]/tbody/tr/td/div')
                for open_house_row in open_house_table:
                    open_house_info = open_house_info + open_house_row.text.replace('\n', ' ') + '\n'

                print open_house_info

                house_info = {'Address':house_addr, 'Price':house_price, 'MLS Number':house_mls_number,
                              'Feature':house_features, 'Details':house_details, 'Open House':open_house_info}
                houses.append(house_info)

                write_file(file_name, '\n\n' + house_url.encode('utf-8') + '\n'
                           + house_addr.encode('utf-8') + '\n'
                            + house_price.encode('utf-8') + '\n'
                            + house_mls_number.encode('utf-8') + '\n'
                            + house_features.replace('\n', ' ').encode('utf-8') + '\n'
                            + house_details.replace('\n', ' ').encode('utf-8') + '\n'
                           + open_house_info.encode('utf-8'))


          next_page = driver.find_element_by_xpath('//*[@id="nextPage"]')
            next_page.click()
            time.sleep(30)

    finally:
        house_json = json.dumps(houses)
        write_json('open_house.json', house_json)






class RealtorCASpider(scrapy.Spider):
    name = "realtorcaspider"

    start_urls = [
    'https://www.realtor.ca/Residential/map.aspx#CultureId=1&ApplicationId=1&RecordsPerPage=9&MaximumResults=9&PropertySearchTypeId=1&PriceMin=500000&PriceMax=1000000&TransactionTypeId=2&StoreyRange=0-0&OwnershipTypeGroupId=1&BuildingTypeId=1&BedRange=3-0&BathRange=2-0&LongitudeMin=-122.84923331284146&LongitudeMax=-122.21202628159146&LatitudeMin=49.02949491490382&LatitudeMax=49.25902216108254&SortOrder=A&SortBy=1&viewState=m&favouritelistingids=17039158,17083903,17239737,17228029,17239664,17257985,17252888&CurrentPage=1&PropertyTypeGroupID=1'
    ]

    from datetime import datetime, date, timedelta

    start_date = date.today().strftime("%m/%d/%Y")

    end_date = (date.today() + timedelta(days=14)).strftime("%m/%d/%Y")

    print(start_date, end_date)

    open_house_url = 'https://www.realtor.ca/Residential/map.aspx#CultureId=1&ApplicationId=1&RecordsPerPage=9&MaximumResults=9&PropertySearchTypeId=1&PriceMin=500000&PriceMax=1000000&TransactionTypeId=2&StoreyRange=2-0&OwnershipTypeGroupId=1&BuildingTypeId=1&ConstructionStyleId=3&BedRange=3-0&BathRange=2-0&LongitudeMin=-122.87910616386483&LongitudeMax=-122.24189913261483&LatitudeMin=49.03026039961354&LatitudeMax=49.25978410832259&SortOrder=A&SortBy=1&OpenHouse=1&OpenHouseStartDate='+ start_date + '&OpenHouseEndDate='+ end_date +'&viewState=m&favouritelistingids=17039158,17083903,17239737,17228029,17239664,17257985,17252888&Longitude=-122.64174005377839&Latitude=49.14514549678261&ZoomLevel=11&CurrentPage=1&PropertyTypeGroupID=1'

    house_search(open_house_url,'open_house.csv')

