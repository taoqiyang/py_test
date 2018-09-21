# -*- coding: utf-8 -*-
import scrapy
import hashlib
import hmac
import random
import time
import json
import pymysql
import logging

domain = 'app.yzgjgs.com'
host = 'http://app.yzgjgs.com:2001/BusService'
secret = bytes("a4001697cb494c03bca607707aefd6d7".encode('utf-8'))


def sign(content):
    content = bytes(content.encode('utf-8'))
    return hmac.new(secret, content, digestmod=hashlib.sha256).hexdigest()


def buildRequest(api, params={}, callback=None):
    random_value = str(random.randint(100, 1000))
    timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    sign_key = sign(timestamp + random_value)
    params['timeStamp'] = timestamp
    params['Random'] = random_value
    params['SignKey'] = sign_key
    return scrapy.FormRequest(host + api,
                              method='GET',
                              formdata=params, callback=callback,
                              dont_filter=True)


def encryptParam(value):
    lt = time.localtime(time.time())
    md = lt.tm_mday
    wd = (lt.tm_wday + 1) % 7
    num = md - wd
    if num <= 10:
        num += 7
    result = list()
    for c in value:
        result.append(chr(ord(c) + num))
    return ''.join(result)


class ExampleSpider(scrapy.Spider):
    name = 'bus'
    allowed_domains = [domain]

    def start_requests(self):
        # yield buildRequest('/Query_AllSubRouteData/', callback=self.parseRoute)
        # yield buildRequest('/Query_NearbyStatInfo/', {'Latitude': '32.4', 'Longitude': '119.36',
        #                                               'Range': '1000000'}, callback=self.parse)
        return self.fix()

    def parse(self, response):
        data = json.loads(response.text)
        try:
            conn = pymysql.connect(host='192.168.200.31', user='root', passwd="123456", db='bus')
            with conn.cursor() as cur:
                cur.execute('delete from station')
                cur.execute('delete from station_route')
                for item in data:
                    cur.execute('insert into station values(%s, %s, %s, %s, %s)',
                                (item['StationID'], item['StationName'], item['StationPostion']['Latitude'],
                                 item['StationPostion']['Longitude'], item['StationMemo']))
                    cur.execute('insert into station_route values(%s, -1)',
                                (item['StationID']))
            conn.commit()
        except Exception:
            conn.rollback()
            logging.error(Exception.__traceback__)
        finally:
            conn.close()

        route_id = encryptParam('-1')
        for station in data:
            yield buildRequest('/Query_ByStationID/', {'StationID': encryptParam(station['StationID']),
                                                       'RouteID': route_id}, callback=self.parse_station_route)

    def parse_station_route(self, response):
        text = response.text
        if text is '':
            return
        route_list = json.loads(response.text)
        print(len(route_list))
        if len(route_list) == 0:
            return
        try:
            conn = pymysql.connect(host='192.168.200.31', user='root', passwd="123456", db='bus')
            with conn.cursor() as cur:
                station_id = route_list[0]['StationID']
                cur.execute('delete from station_route where StationID=%s and RouteID=-1', station_id)
                for route in route_list:
                    cur.execute('insert into station_route values(%s, %s)',
                                (station_id, route['RouteID']))
            conn.commit()
        except Exception:
            conn.rollback()
            logging.error(Exception.__traceback__)
        finally:
            conn.close()

    def parseRoute(self, response):
        data = json.loads(response.text)
        route_list = data['RouteList']
        try:
            conn = pymysql.connect(host='192.168.200.31', user='root', passwd="123456", db='bus')
            with conn.cursor() as cur:
                cur.execute('delete from route')
                for route in route_list:
                    cur.execute('insert into route values(%s, %s, %s, %s)',
                                (route['RouteID'], route['RouteName'],
                                 route['IsHaveSubRouteCombine'], route['RouteNameExt']))
            conn.commit()
        except Exception:
            conn.rollback()
            logging.error(Exception.__traceback__)
        finally:
            conn.close()

    def fix(self):
        try:
            conn = pymysql.connect(host='192.168.200.31', user='root', passwd="123456", db='bus')
            with conn.cursor() as cur:
                cur.execute('select StationID from station_route where RouteID = -1')
                route_id = encryptParam('-1')
                for item in cur.fetchall():
                    yield buildRequest('/Query_ByStationID/', {'StationID': encryptParam(str(item[0])),
                                                               'RouteID': route_id}, callback=self.parse_station_route)
            conn.commit()
        except Exception:
            conn.rollback()
            logging.error(Exception.__traceback__)
        finally:
            conn.close()
