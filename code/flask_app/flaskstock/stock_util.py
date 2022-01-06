#####
# Stock Utility Functions
#####

import requests
import sys
import ssl
from bs4 import BeautifulSoup, element


def get_headers():
    # return {'authority': 'www.nseindia.com',
    #         'cache-control': 'max-age=0',
    #         'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    #         'sec-ch-ua-mobile': '?0',
    #         'upgrade-insecure-requests': '1',
    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    #         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #         'sec-fetch-site': 'none',
    #         'sec-fetch-mode': 'navigate',
    #         'sec-fetch-user': '?1',
    #         'sec-fetch-dest': 'document',
    #         'accept-language': 'en-US,en;q=0.9',
    #         }
    return {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) '
                          'Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}

    # return {'Accept': '*/*',
    #         'Accept-Language': 'en-US,en;q=0.5',
    #         'Host': 'www1.nseindia.com',
    #         'User-Agent': 'Mnseindiaozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    #         'X-Requested-With': 'XMLHttpRequest'
    #         }

cookiee = None
def get_cookie():
    baseurl = "https://nseindia.com/"

    session = requests.Session()
    request = session.get(baseurl, headers=get_headers(), timeout=15)
    cookies = dict(request.cookies)
    global cookiee
    cookiee = cookies
    print('cookies: ', cookies)
    return cookies


def place_request(url):
    print('url: ', url)
    global cookiee
    if cookiee is None:
        cookiee = get_cookie()
    print('global cookiee: ', cookiee)
    session = requests.Session()
    response = session.get(url, headers=get_headers(), timeout=15, cookies=cookiee)
    return response


def get_symbols(url):
    indices, stocks = [], []
    try:
        symbols_information: requests.Response = requests.get(url, headers=get_headers())
        symbols_information_soup: BeautifulSoup = BeautifulSoup(symbols_information.content, "html.parser")
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
        print(err, sys.exc_info()[0], "19")
    except IndexError as err:
        print(err, sys.exc_info()[0], "20")
    print('equity derivative symbols:')
    print(indices)
    print(stocks)
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
