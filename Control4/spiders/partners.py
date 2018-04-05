# -*- coding: utf-8 -*-
import scrapy
import json
import time
import requests

from urllib import urlencode
from scrapy.selector import Selector


class PartnersSpider(scrapy.Spider):
    name = 'partners'

    def start_requests(self):
        url = 'https://www.control4.com/dealer_locator'
        return [scrapy.http.Request(url, callback=self.parse_countries)]

    def parse_countries(self, response):
        countries = response.selector.xpath('//select[@id="selected-country"]/option[position()>1]/text()').extract()

        partners = []
        for country in countries:
            url = "https://maps.googleapis.com/maps/api/geocode/json"

            location = json.loads(requests.get(url, params={
                'address':country, 
                'alert':False, 
                'key':'AIzaSyDJkTAdKTUcQ27bUkR_XmQ2Z3Gd01xRsXA'
            }).content)
            loc = location.get('results')[0].get('geometry').get('location')
            partners += self.get_partners(loc)

        return partners


    def get_partners(self, location):
        url = "https://www.control4.com/dealer_locator/query"
        page = 0
        data = location
        data['page'] = page
        partner_list = []
        partners = json.loads(requests.post(url, data=data).content)

        while(len(partners)):
            page += 1
            data['page'] = page
            partners = json.loads(requests.post(url, data=data).content)

            for partner in partners:
                partner['address_city'] = partner['address']['city']
                partner['address_country'] = partner['address']['country']
                partner['address_line1'] = partner['address']['line1']
                partner['address_line2'] = partner['address']['line2']
                partner['address_name'] = partner['address']['name']
                partner['address_postal'] = partner['address']['postalCode']
                partner['address_state'] = partner['address']['stateProvince']
                del partner['address']
                partner_list.append(partner)

        return partner_list
