#####
# Stock Utility Functions
#####

import requests
import ssl
import subprocess
import os, sys, json
from bs4 import BeautifulSoup, element

import logging

blank_response = '''{
	"records": {
		"expiryDates": [
		],
		"data": [
			{
				"strikePrice": 0,
				"expiryDate": "",
				"PE": {
					"strikePrice": 0,
					"expiryDate": "",
					"underlying": "",
					"identifier": "",
					"openInterest": 0,
					"changeinOpenInterest": 0,
					"pchangeinOpenInterest": 0,
					"totalTradedVolume": 0,
					"impliedVolatility": 0,
					"lastPrice": 0.0,
					"change": 0,
					"pChange": 0,
					"totalBuyQuantity": 0,
					"totalSellQuantity": 0,
					"bidQty": 0,
					"bidprice": 0.0,
					"askQty": 0,
					"askPrice": 0,
					"underlyingValue": 0.0
				}
			},
			{
				"strikePrice": 0,
				"expiryDate": "",
				"CE": {
					"strikePrice": 0,
					"expiryDate": "",
					"underlying": "",
					"identifier": "",
					"openInterest": 0,
					"changeinOpenInterest": 0,
					"pchangeinOpenInterest": 0,
					"totalTradedVolume": 0,
					"impliedVolatility": 0,
					"lastPrice": 0.0,
					"change": 0,
					"pChange": 0,
					"totalBuyQuantity": 0,
					"totalSellQuantity": 0,
					"bidQty": 0,
					"bidprice": 0.0,
					"askQty": 0,
					"askPrice": 0,
					"underlyingValue": 0.0
				}
			},
			{
				"strikePrice": 0,
				"expiryDate": "",
				"CE": {
					"strikePrice": 0,
					"expiryDate": "",
					"underlying": "",
					"identifier": "",
					"openInterest": 0,
					"changeinOpenInterest": 0,
					"pchangeinOpenInterest": 0,
					"totalTradedVolume": 0,
					"impliedVolatility": 0,
					"lastPrice": 0,
					"change": 0,
					"pChange": 0,
					"totalBuyQuantity": 0,
					"totalSellQuantity": 0,
					"bidQty": 0,
					"bidprice": 0,
					"askQty": 0,
					"askPrice": 0,
					"underlyingValue": 0.0
				},
				"PE": {
					"strikePrice": 0,
					"expiryDate": "",
					"underlying": "",
					"identifier": "",
					"openInterest": 0,
					"changeinOpenInterest": 0,
					"pchangeinOpenInterest": 0,
					"totalTradedVolume": 0,
					"impliedVolatility": 0,
					"lastPrice": 0,
					"change": 0,
					"pChange": 0,
					"totalBuyQuantity": 0,
					"totalSellQuantity": 0,
					"bidQty": 0,
					"bidprice": 0.0,
					"askQty": 0,
					"askPrice": 0.0,
					"underlyingValue": 0.0
				}
			}
		],
		"timestamp": "",
		"underlyingValue": 0.0,
		"strikePrices": [
		]
	},
	"filtered": {
		"data": [
			{
				"strikePrice": 0,
				"expiryDate": "",
				"CE": {
					"strikePrice": 0,
					"expiryDate": "",
					"underlying": "",
					"identifier": "",
					"openInterest": 0,
					"changeinOpenInterest": 0,
					"pchangeinOpenInterest": 0,
					"totalTradedVolume": 0,
					"impliedVolatility": 0,
					"lastPrice": 0.0,
					"change": 0.0,
					"pChange": 0.0,
					"totalBuyQuantity": 0,
					"totalSellQuantity": 0,
					"bidQty": 0,
					"bidprice": 0.0,
					"askQty": 0,
					"askPrice": 0.0,
					"underlyingValue": 0.0
				},
				"PE": {
					"strikePrice": 0,
					"expiryDate": "",
					"underlying": "",
					"identifier": "",
					"openInterest": 0,
					"changeinOpenInterest": 0,
					"pchangeinOpenInterest": 0.0,
					"totalTradedVolume": 0,
					"impliedVolatility": 0.0,
					"lastPrice": 0.0,
					"change": -0.0,
					"pChange": -0.0,
					"totalBuyQuantity": 0,
					"totalSellQuantity": 0,
					"bidQty": 0,
					"bidprice": 0.0,
					"askQty": 0,
					"askPrice": 0.0,
					"underlyingValue": 0.0
				}
			}
		],
		"CE": {
			"totOI": 0,
			"totVol": 0
		},
		"PE": {
			"totOI": 0,
			"totVol": 0
		}
	}
}'''


def get_headers():
    return {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) '
                          'Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}


cookiee = None


def get_cookie():
    baseurl = "https://nseindia.com/"

    session = requests.Session()
    request = session.get(baseurl, headers=get_headers(), timeout=15)
    cookies = dict(request.cookies)
    global cookiee
    cookiee = cookies
    logging.info(f'cookies: [{cookies}]')
    return cookies


def place_request_V1(url):
    '''
    deprecated function

    :param url:
    :return:
    '''
    logging.info(f'url: [{url}]')
    global cookiee
    if cookiee is None:
        cookiee = get_cookie()
    logging.info(f'global cookiee: [{cookiee}]')
    session = requests.Session()
    response = session.get(url, headers=get_headers(), timeout=15, cookies=cookiee)
    return response


def place_request(url):
    '''
    places curl request through a python-shell to fetch the option-data
    :param url:
    :return:
    '''
    subprocess.call(
        f'curl "{url}" -H "authority: beta.nseindia.com" -H "cache-control: max-age=0" -H "dnt: 1" -H "upgrade-insecure-requests: 1" -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36" -H "sec-fetch-user: ?1" -H "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" -H "sec-fetch-site: none" -H "sec-fetch-mode: navigate" -H "accept-encoding: gzip, deflate, br" -H "accept-language: en-US,en;q=0.9,hi;q=0.8" --compressed  -o /home/ubuntu/flask_app/curl_output.txt',
        shell=True)

    with open("/home/ubuntu/flask_app/curl_output.txt", "r") as f:
        var = f.read()
        try:
            return json.loads(var)
        except:
            logging.info(f'curl response : [{var}]')
            return json.loads(blank_response)


def get_symbols(url):
    indices, stocks = [], []
    try:
        subprocess.call(
            f'curl "{url}" -H "authority: beta.nseindia.com" -H "cache-control: max-age=0" -H "dnt: 1" -H "upgrade-insecure-requests: 1" -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36" -H "sec-fetch-user: ?1" -H "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" -H "sec-fetch-site: none" -H "sec-fetch-mode: navigate" -H "accept-encoding: gzip, deflate, br" -H "accept-language: en-US,en;q=0.9,hi;q=0.8" --compressed  -o /home/ubuntu/flask_app/curl_scrap.html',
            shell=True)
        with open('/home/ubuntu/flask_app/curl_scrap.html') as content:
            symbols_information_soup: BeautifulSoup = BeautifulSoup(content, "html.parser")
            symbols_table: element.Tag = symbols_information_soup.findChildren('table')[0]

            symbols_table_rows: list[element.Tag] = list(symbols_table.findChildren(['th', 'tr']))
            symbols_table_rows_str: list[str] = ['' for _ in range(len(symbols_table_rows) - 1)]
            for column in range(len(symbols_table_rows) - 1):
                symbols_table_rows_str[column] = str(symbols_table_rows[column])
            divider_row: str = '<tr>\n' \
                               '<td colspan="3"><strong>Derivatives on Individual Securities</strong></td>\n' \
                               '</tr>'
            for column in range(4, symbols_table_rows_str.index(divider_row) + 1):
                cells: element.ResultSet = symbols_table_rows[column].findChildren('td')
                column: int = 0
                for cell in cells:
                    if column == 2:
                        indices.append(cell.string)
                    column += 1
            for column in reversed(range(symbols_table_rows_str.index(divider_row) + 1)):
                symbols_table_rows.pop(column)
            for row in symbols_table_rows:
                cells: element.ResultSet = row.findChildren('td')
                column: int = 0
                for cell in cells:
                    if column == 2:
                        stocks.append(cell.string)
                    column += 1
    except Exception as err:
        logging.info(err, sys.exc_info()[0], "19")
    except IndexError as err:
        logging.info(err, sys.exc_info()[0], "20")
    logging.info('equity derivative symbols:')
    logging.info(indices)
    logging.info(stocks)
    return {'indices': indices, 'stocks': stocks}


def unused_replace_0_with_hyphen(formatted_data):
    attr_list = ['openInterest', 'changeinOpenInterest', 'totalTradedVolume',
                 'impliedVolatility', 'lastPrice', 'change', 'bidQty', 'bidprice', 'askPrice', 'askQty']
    for data in formatted_data['records']['data']:
        ce = data.get('CE')
        pe = data.get('PE')
        if ce is not None:
            for attr in attr_list:
                if ce[attr] == 0:
                    ce[attr] = '-'
        if pe is not None:
            for attr in attr_list:
                if pe[attr] == 0:
                    pe[attr] = '-'
    return formatted_data
