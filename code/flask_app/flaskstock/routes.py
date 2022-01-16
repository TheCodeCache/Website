import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskstock import app, db, bcrypt
from flaskstock.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskstock.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

from flaskstock import stock_util as util
from flaskstock import stock_helper as helper

from datetime import datetime

import logging

logging.basicConfig(filename='equity-updates.log',
                    level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

"""
 this dictionary grows in size over the time,
 hence, we may need to put some kind of threshold,
 or may be LRU cache policy would work fine!
 Analyze it more!!
"""
option_data_in_use = {}

posts = [
    {
        'author': 'Manoranjan',
        'title': 'Stock - Tech. Analysis',
        'content': 'price prediction through graphs/charts',
        'date_posted': 'Oct 04, 2021'
    },
    {
        'author': 'Manoranjan',
        'title': 'Stock - Business Model',
        'content': 'screener.in for fundamental analysis',
        'date_posted': 'Nov 16, 2021'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/optiontest")
@login_required
def optiontest():
    data = helper.get_option_data()

    expiry_dates = helper.get_expiry_dates(data)
    strike_prices = helper.get_strike_prices(data)

    symbols = util.get_symbols(
        f"https://www.nseindia.com/products-services/equity-derivatives-list-underlyings-information")
    logging.info(symbols)

    my_date = datetime.now()
    timestamp = my_date.strftime('%d-%b-%Y %H:%M:%S')

    return render_template('optiontest.html',
                           title='Option Test',
                           symbol='NIFTY',
                           timestamp=timestamp,
                           indices_symbols=symbols['indices'],
                           stocks_symbols=symbols['stocks'],
                           expiry_dates=expiry_dates,
                           strike_prices=strike_prices
                           )


# url = f"https://www.nseindia.com/api/option-chain-equities?symbol=RELIANCE"
# url = f"https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
# url = f"https://www.nseindia.com/api/quote-derivative?symbol=RELIANCE"
# url = f"https://www.nseindia.com/api/quote-equity?symbol=RELIANCE"
# url = f"https://www.nseindia.com/api/quote-equity?symbol=RELIANCE&section=trade_info"
# url = f"https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O"

# nsepython library
# documentation: f"https://forum.unofficed.com/t/nsepython-documentation/376"
# market status
# https://www.nseindia.com/api/marketStatus

@app.route("/option")
@login_required
def option():
    logging.info('/option path invoked')
    data = helper.get_option_data()

    expiry_dates = helper.get_expiry_dates(data)
    strike_prices = helper.get_strike_prices(data)

    logging.info(f'fetching symbols...')
    symbols = util.get_symbols(
        f"https://www.nseindia.com/products-services/equity-derivatives-list-underlyings-information")
    logging.info(f'symbols: {symbols}')

    my_date = datetime.now()
    timestamp = my_date.strftime('%d-%b-%Y %H:%M:%S')

    return render_template('option.html',
                           title='Option Chain - EquityUpdates',
                           symbol='NIFTY',
                           timestamp=timestamp,
                           indices_symbols=symbols['indices'],
                           stocks_symbols=symbols['stocks'],
                           expiry_dates=expiry_dates,
                           strike_prices=strike_prices
                           )


@app.route("/ajax/<string:symbol>/<string:tag>")
def ajax(symbol, tag):
    logging.info(f'requesting option-data for symbol: {symbol} and tag: {tag}')

    data = helper.get_option_data(symbol, tag)
    logging.info(data)
    float_attrs = ['change']
    formatted_data = helper.format_float_values(data, float_attrs)
    # formatted_data = util.replace_0_with_hyphen(formatted_data)
    logging.info(formatted_data)
    global option_data_in_use
    option_data_in_use[symbol] = formatted_data

    total_dict = helper.get_total_symbol(formatted_data)
    logging.info(total_dict)
    market_value = formatted_data['records']['underlyingValue']
    logging.info(f'market_value: [{market_value}]')

    expiry_dates = helper.get_expiry_dates(formatted_data)
    strike_prices = helper.get_strike_prices(formatted_data)

    filter_data = helper.filter_by_expiry_date(formatted_data, expiry_dates[0]) if expiry_dates else []
    # logging.info(filter_data)

    html = render_template("section.html",
                           symbol=symbol,
                           market_value=market_value,
                           option_data=filter_data,
                           total_dict=total_dict)

    return {'expiry_dates': expiry_dates,
            'strike_prices': strike_prices,
            'market_value': market_value,
            'html': html}


@app.route("/filter_path/<string:symbol>/<string:tag_value>/<string:tag_name>")
def filter_path(symbol, tag_value, tag_name):
    """
    # TODO these params into dictionary params
    # TODO Analyze filtered_records from the nse-API response json
    :param symbol:
    :param tag_value:
    :param tag_name:
    :return:
    """

    logging.info(f"symbol: {symbol}, \
            tag_value: {tag_value}, tag_name: {tag_name}")

    if symbol in option_data_in_use:
        logging.info('OPTION-DATA HAS BEEN FOUND IN GLOBAL SPACE')
        formatted_data = option_data_in_use[symbol]
    else:
        logging.info('OPTION-DATA NOT FOUND IN GLOBAL SPACE')
        formatted_data = None

    market_value = formatted_data['records']['underlyingValue']

    if tag_name == 'expiry_date':
        filter_data = helper.filter_by_expiry_date(formatted_data, tag_value)
    elif tag_name == 'strike_price':
        filter_data = helper.filter_by_strike_price(formatted_data, tag_value)
    else:
        filter_data = None
    total_dict = helper.get_total_filter(filter_data)

    return render_template("section.html",
                           option_data=filter_data,
                           market_value=market_value,
                           total_dict=total_dict)
