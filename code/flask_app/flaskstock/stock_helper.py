#####
# Stock Helper Functions
#####
from flaskstock import stock_util as util
import json
import logging


def filter_by_expiry_date(data, date):
    recs = [rec for rec in data['records']['data'] if rec['expiryDate'] == date]
    return recs


def filter_by_strike_price(data, price):
    recs = [rec for rec in data['records']['data'] if rec['strikePrice'] == int(price)]
    return recs


def get_total_symbol(data):
    total_dict = {'ce': {'vol': data['filtered']['CE']['totVol'], 'oi': data['filtered']['CE']['totOI']},
                  'pe': {'vol': data['filtered']['PE']['totVol'], 'oi': data['filtered']['PE']['totOI']}}
    return total_dict


def get_total_filter(filtered_data):
    ce_sum_oi, pe_sum_oi, ce_sum_vol, pe_sum_vol = 0, 0, 0, 0
    for data in filtered_data:
        pe = data.get('PE')
        ce = data.get('CE')
        if pe is not None:
            pe_sum_oi += pe['openInterest']
            pe_sum_vol += pe['totalTradedVolume']
        if ce is not None:
            ce_sum_oi += ce['openInterest']
            ce_sum_vol += ce['totalTradedVolume']
    total_dict = {'ce': {'vol': ce_sum_vol, 'oi': ce_sum_oi},
                  'pe': {'vol': pe_sum_vol, 'oi': pe_sum_oi}}
    return total_dict


def format_float_values(formatted_data, attr_list):
    for data in formatted_data['records']['data']:
        pe = data.get('PE')
        ce = data.get('CE')
        for attr in attr_list:
            if pe is not None:
                pe[attr] = round(pe[attr], 2)
            if ce is not None:
                ce[attr] = round(ce[attr], 2)
    return formatted_data


def get_expiry_dates(data):
    return data['records']['expiryDates']


def get_strike_prices(data):
    return sorted(data['records']['strikePrices'])


def get_option_data(symbol='NIFTY', tag='indices'):
    if tag == 'indices':
        word = 'indices'
    elif tag == 'stocks':
        word = 'equities'
    else:
        word = None

    url = f"https://www.nseindia.com/api/option-chain-{word}?symbol={symbol}"
    response = util.place_request(url)
    logging.info('option_data received:')
    # logging.info(f'option_data: {response}')
    # logging.info(f'option_data_type: {type(response)}')
    # data = json.loads(response.text)
    return response
