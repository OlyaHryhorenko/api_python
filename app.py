#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import logging
import os
import random
import time
import pytz
import glob
import string
import requests
from pytz import timezone
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
from functools import wraps
from smtplib import SMTP_SSL, SMTP
from time import gmtime, strftime
from MySQLdb import escape_string

import magic
import pygeoip
from flask import (Flask, Response, abort, jsonify, redirect, render_template,
                   request, send_file, session, url_for, Markup, make_response)
from flask_mail import Mail, Message
from paypal import PayPalConfig, PayPalInterface
from werkzeug import secure_filename
from random import randint

from flask.ext.assets import Environment, Bundle
from flask.ext.cache import Cache
from flask_cors import CORS, cross_origin

from apps.models.wrapper import Wrapper

from apps.models.customer import Customer
from apps.models.dashboard import Dashboard
from apps.models.events import Events
from apps.models.files import Files
from apps.models.messages import Messages
from apps.models.orders import Orders
from apps.models.transactions import Transactions
from apps.models.turbosms import Turbosms
from apps.models.users import Users
from apps.models.prices import Prices
from apps.models.sys_const import SysConst
from apps.models.api import Api
from apps.models.adm_seo_system import AdmSeoSystem
from apps.models.paypalerr import PayPalErr
from apps.models.templateletter import TemlateLetter
from apps.models.createsitemap import CreateSiteMap
from apps.models.decorators import crossdomain
from apps.models.revisions import Revisions
from apps.models.subject import Subject
from apps.models.sites import Sites
from apps.models.typeofpaper import OrderAssignment
from apps.models.extraorders import Extraorders
from apps.utils.utils import delta_date, GetListFile, convert_pp_response_to_dict

# Prodaction #1

config = PayPalConfig(
    API_USERNAME="paypal_api1.bryteq.com",
    API_PASSWORD="AD48MC6JDN5TMBPE",
    API_SIGNATURE="AiPC9BjkCyDFQXbSkoZcgqH3hpacAz-3lWgKg-sdhUdkzsy3xKe3oKv2",
    API_ENDPOINT="https://api-3t.paypal.com/nvp",
    API_ENVIRONMENT="PRODUCTION",
    API_AUTHENTICATION_MODE='3TOKEN')

interface = PayPalInterface(config=config)

# ----------------------------------------------------------------------------
# File Settings
# ----------------------------------------------------------------------------
ALLOWED_EXTENSIONS = set(
    ['txt', 'zip', 'doc', 'docx', 'xls', 'xlsx', 'rtf', 'jpeg', 'png', 'gif', 'ppt', 'pptx', 'csv', 'pdf', 'jpg',
     'odt'])
ALLOWED_FILETYPE = set(['text', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'excel', 'word', 'opendocument'])

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
DOWNLOAD_FOLDER = os.path.join(APP_ROOT, 'wr_uploads')
LOG_FOLDER = os.path.join(APP_ROOT, 'log')
LOG_FILE = os.path.join(LOG_FOLDER, 'app.log')
ADM_TEMPLATE_FOLDER = 'adm_template/'
CUSTOM_TEMPLATE_FOLDER = 'custom_template/'

URL_SYSTEM = "http://_writing-center.com/api/extra_orders/writer_surcharge"
X_TOKEN_SYSTEM = "_1677cf493e4b41a299fe0b6a4984048d"

# Log config
# logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
# ----------------------------------------------------------------------------

app = Flask(__name__)
CORS(app, support_credentials=True)
mail = Mail(app)
# app.debug = True
app.secret_key = '2B5L7Vyv5trgrg56b590i1Vejpny2KtxVg9IPyQ'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.before_request(lambda: setattr(session, 'permanent', True))
app.permanent_session_lifetime = datetime.timedelta(days=64)
site_id = 1
site_name = ''
site_mail = ''
site_mail_revisions = ''
site_mail_revisions_pass = ''
site_noreply_mail = ''
site_noreply_pass = ''
site_pass = ''

bundles = {

    'orderinfo_js': Bundle(
        'js/fileinput.js',
        'js/jquery.bootstrap-touchspin.js',
        'js/bootstrap-datetimepicker_new.js',
        output='gen/orderinfo.js',
        filters='jsmin'),

    'orderinfo2_js': Bundle(
        'js/revdt.js',
        'js/editorder.js',
        output='gen/orderinfo2.js',
        filters='jsmin'),

    'dashboard_js': Bundle(
        'js/fileinput.js',
        'js/dashboard_scripts.js',
        output='gen/dashboard.js',
        filters='jsmin'),

    'scripts_js': Bundle(
        'js/jquery.1.9.1.js',
        'js/jquery.carouselHeight.js',
        'js/bootstrap.js',
        'js/legacy.min.js',
        'js/custombox.min.js',
        'js/bootstrap-select.js',
        'js/moment.js',
        'js/bootstrap-datetimepicker.js',
        'js/jquery.form.js',
        'js/url.min.js',
        'js/calc.js',
        'js/order_scripts.js',
        'js/app.js',
        'js/bootbox.min.js',
        'js/utils.js',
        'js/media-paragraph.js',
        'js/zopim.js',
        'js/google_counter.js',
        'js/yand_metr_counter.js',
        'js/send_metrik_yandex.js',
        'js/copyright.js',
        output='gen/scripts.js',
        filters='jsmin'),

    'main_css': Bundle(
        'css/bootstrap-select.css',
        'css/bootstrap-datetimepicker.css',
        'css/custombox.min.css',
        'css/reset.css',
        'css/bootstrap.css',
        'css/fonts.css',
        'css/custom.css',
        'css/media-paragraph.css',
        output='gen/mainstyle.css',
        filters='cssmin'),

    'orderinfo_css': Bundle(
        'css/fileinput.min.css',
        'css/jquery.bootstrap-touchspin.css',
        'css/dropzone.css',
        'css/orderinfo_style.css',
        output='gen/orderinfo.css',
        filters='cssmin'),

    'dashboard_css': Bundle(
        'css/fileinput.min.css',
        output='gen/dashboard.css',
        filters='cssmin')
}

assets = Environment(app)

assets.register(bundles)

cache = Cache(config={'CACHE_TYPE': 'simple'})

cache.init_app(app)


def login_required(f):
    @wraps(f)
    def wrap():
        if 'logged_in' in session:
            return f()
        else:
            return redirect(url_for('login_form'))

    return wrap


def login_required_adm(f):
    @wraps(f)
    def wrap():
        if 'logged_in_adm' in session:
            return f()
        else:
            abort(404)

    return wrap


@app.before_first_request
def SetStartSettings():
    # ##logging.info("secret_key = {0}".format(str(SysConst(APP_ROOT).Get_Sys_Const("secret_key"))))
    app.secret_key = SysConst(APP_ROOT).Get_Sys_Const("secret_key")

    # ##logging.info("site_id = {0}".format(str(SysConst(APP_ROOT).Get_Sys_Const("site_id"))))


    # ##logging.info("site_id 2 = {0}".format(site_id))

    # ##logging.info("site_name = {0}".format(str(SysConst(APP_ROOT).Get_Sys_Const("site_name"))))
    global site_name
    site_name = SysConst(APP_ROOT).Get_Sys_Const("site_name")

    # ##logging.info("site_mail = {0}".format(str(SysConst(APP_ROOT).Get_Sys_Const("site_mail"))))
    global site_mail
    site_mail = SysConst(APP_ROOT).Get_Sys_Const("site_mail")

    # ##logging.info("site_mail_revisions = {0}".format(str(SysConst(APP_ROOT).Get_Sys_Const("site_mail_revisions"))))
    global site_mail_revisions
    site_mail_revisions = SysConst(APP_ROOT).Get_Sys_Const("site_mail_revisions")

    # ##logging.info("site_mail_revisions = {0}".format(str(SysConst(APP_ROOT).Get_Sys_Const("site_mail_revisions"))))
    global site_mail_revisions_pass
    site_mail_revisions_pass = SysConst(APP_ROOT).Get_Sys_Const("site_mail_revisions_pass")

    # ##logging.info("site_pass = {0}".format(str(SysConst(APP_ROOT).Get_Sys_Const("site_pass"))))
    global site_pass
    site_pass = SysConst(APP_ROOT).Get_Sys_Const("site_pass")

    # ##logging.info("site_noreply_mail = {0}".format(str(SysConst(APP_ROOT).Get_Sys_Const("noreply_mail"))))
    global site_noreply_mail
    site_noreply_mail = SysConst(APP_ROOT).Get_Sys_Const("noreply_mail")

    # ##logging.info("site_noreply_pass = {0}".format(str(SysConst(APP_ROOT).Get_Sys_Const("noreply_pass"))))
    global site_noreply_pass
    site_noreply_pass = SysConst(APP_ROOT).Get_Sys_Const("noreply_pass")

    config = PayPalConfig(
        API_USERNAME=str(SysConst(APP_ROOT).Get_Sys_Const("API_USERNAME")),
        API_PASSWORD=str(SysConst(APP_ROOT).Get_Sys_Const("API_PASSWORD")),
        API_SIGNATURE=str(SysConst(APP_ROOT).Get_Sys_Const("API_SIGNATURE")),
        API_ENDPOINT=str(SysConst(APP_ROOT).Get_Sys_Const("API_ENDPOINT")),
        API_ENVIRONMENT=str(SysConst(APP_ROOT).Get_Sys_Const("API_ENVIRONMENT")),
        API_AUTHENTICATION_MODE=str(SysConst(APP_ROOT).Get_Sys_Const("API_AUTHENTICATION_MODE")))
    global interface
    interface = PayPalInterface(config=config)

    global ALLOWED_EXTENSIONS
    ALLOWED_EXTENSIONS = set((str(SysConst(APP_ROOT).Get_Sys_Const("ALLOWED_EXTENSIONS"))).split(','))
    # ##logging.info("ALLOWED_EXTENSIONS = {0}".format(ALLOWED_EXTENSIONS))

    global ALLOWED_FILETYPE
    ALLOWED_FILETYPE = set((str(SysConst(APP_ROOT).Get_Sys_Const("ALLOWED_FILETYPE"))).split(','))
    # ##logging.info("ALLOWED_FILETYPE = {0}".format(ALLOWED_FILETYPE))



@app.errorhandler(404)
def handel_404(error):
    page_url = "'/404.html','/404'"
    list_contents = SysConst(APP_ROOT).GetHTML_Content_Pages(page_url)
    list_contents_include = SysConst(APP_ROOT).GetHTML_Include_Content_Pages()
    template_pages = SysConst(APP_ROOT).Get_Template_Pages(page_url)
    return render_template(template_pages,
                           list_contents=list_contents,
                           list_contents_include=list_contents_include
                           ), 404
    # ##return render_template('404.html'), 404


@app.errorhandler(500)
def handel_500(error):
    page_url = "'/500.html','/500'"
    template_pages = SysConst(APP_ROOT).Get_Template_Pages(page_url)
    return render_template('500.html',
                           ), 500
    # ##return render_template('500.html'), 500


# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Mail Send #
def send_mail(login, password, from_address, to_address, subject, text, html, atach_file="", atach_file_name=""):
    """
    function for send mail
    :param login: (string) login for notification on mail server
    :param password: (string) password for notification on mail server
    :param from_address: (string) mail from sends
    :param to_address: (string) mail to sends
    :param subject: (string) text subject letter
    :param text: (string) text body
    :param html: (string) html body
    :param atach_file: (list string) list with files
    :param atach_file_name: (list string) list with good name files
    :return: send message
    """
    # Compose message
    try:
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject

        if (text != ""):
            msg_send = TemlateLetter().get_template_letter(subject, "", text,
                                                           ShortSiteName(site_name),
                                                           site_mail,
                                                           site_name)
            text = msg_send
            part1 = MIMEText(text, 'plain')
            msg.attach(part1)

        if (html != ""):
            msg_send = TemlateLetter().get_template_letter(subject, "", html,
                                                           ShortSiteName(site_name),
                                                           site_mail,
                                                           site_name)
            html = msg_send
            part2 = MIMEText(html, 'html')
            msg.attach(part2)

        if (atach_file != ""):
            atach_file_ = atach_file.split(':')
            atach_file_name_ = atach_file_name.split(':')
            for rc in range(len(atach_file_)):
                if (len(atach_file_[rc]) > 0):
                    part = MIMEBase('application', "octet-stream")
                    part.set_payload(open(os.path.join(UPLOAD_FOLDER, atach_file_[rc]), "rb").read())
                    # ##logging.info("atachment file = {0}".format(os.path.join(UPLOAD_FOLDER,atach_file_[rc])))
                    Encoders.encode_base64(part)
                    file_name_for_mail = "file_nonename"
                    try:
                        file_name_for_mail = atach_file_name_[rc]
                    except Exception, e:
                        # ##file_name_for_mail="{0}_Client\'s file name{1}".format(str(rc+1),os.path.splitext(atach_file_[rc])[1][1:].strip().lower())
                        file_name_for_mail = str(atach_file_[rc]).lower()
                    part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(file_name_for_mail))
                    msg.attach(part)

        # Send mail
        # smtp = SMTP_SSL()
        smtp = SMTP()
        smtp.connect("mbxsrv.com")
        smtp.login(login, password)
        smtp.sendmail(from_address, to_address, msg.as_string())
        # ##logging.info("from_address = {0}".format(from_address))
        smtp.quit()
    except Exception, e:
        logging.info('[e] send_mail ERROR = {0}'.format(e))


def send_mail_from_server(subject, to_address, body, html):
    msg = Message(subject, sender=site_mail, recipients=[to_address])
    msg.body = body
    msg_send = TemlateLetter().get_template_letter(subject, "Hello!", html, ShortSiteName(site_name), site_mail,
                                                   site_name)
    msg.html = html
    mail.send(msg)


# ----------------------------------------------------------------------------


@app.route("/paypal/redirect", methods=['GET'])
@cross_origin(supports_credentials=True)
def paypal_redirect():
    orderid = request.args.get('orderid')
    # ##price = request.args.get('price')
    price = 0
    id_order = Orders().get_id_by_uid(orderid, session['site_id'])[0].get('id')
    userorders = list(Orders().get_all_ordersid_byuser(session['id'], session['site_id']))
    xx = [int(x['id']) for x in userorders]
    if int(id_order) in xx:
        info_order = Orders().get_full_order(id_order, session['site_id'])[0]
        status = info_order.get('id_order_status')
        if str(status) == '10':
            wrap = Wrapper()
            if not Extraorders(wrap).can_pay_extraoder(id_order):
                return redirect(url_for('dashboard'))
            price = info_order.get('final_order_surcharge')
            id_extra_price = info_order.get('id_extr_ord')
            orderid = "_".join((orderid, str(id_extra_price)))
        else:
            price = info_order.get('price')
        kw = {
            'returnurl': url_for('paypal_confirm', _external=True),
            'cancelurl': url_for('paypal_cancel', _external=True),
            'NOSHIPPING': 1,
            'LOGOIMG': "{0}{1}".format(SysConst(APP_ROOT).Get_Sys_Const("site_name"), '/static/img/paypal_logo.jpg'),
            'BRANDNAME': ShortSiteName(site_name),
            'CARTBORDERCOLOR': '202020',
            'METHOD': 'SetExpressCheckout',
            'PAYMENTREQUEST_0_PAYMENTACTION': 'sale',
            'PAYMENTREQUEST_0_INVNUM': orderid,
            'PAYMENTREQUEST_0_CUSTOM': orderid,
            'L_PAYMENTREQUEST_0_NAME0': 'Order #' + orderid,
            'L_PAYMENTREQUEST_0_DESC0': orderid,
            'L_PAYMENTREQUEST_0_AMT0': price,
            'L_PAYMENTREQUEST_0_QTY0': '1',
            'PAYMENTREQUEST_0_ITEMAMT': price,
            'PAYMENTREQUEST_0_AMT': price,
            'PAYMENTREQUEST_0_CURRENCYCODE': 'USD',
            'ALLOWNOTE': 0
        }
        setexp_response = interface.set_express_checkout(**kw)
        return redirect(interface.generate_express_checkout_redirect_url(setexp_response.token))
    else:
        abort(404)


@app.route("/paypal/confirm")
def paypal_confirm():
    getexp_response = interface.get_express_checkout_details(token=request.args.get('token', ''))
    if getexp_response['ACK'] == 'Success':
        return redirect(url_for('paypal_do', token=getexp_response['TOKEN']))
    else:
        return redirect(url_for('dashboard'))


@app.route("/paypal/do/<string:token>")
def paypal_do(token):
    try:
        # ID Extraorder after id order "_{}"
        MASK_EXTRAORDER = "_{}"
        getexp_response = interface.get_express_checkout_details(token=token)
        kw = {
            'amt': getexp_response['AMT'],
            'paymentaction': 'Sale',
            'payerid': getexp_response['PAYERID'],
            'token': token,
            'currencycode': getexp_response['CURRENCYCODE']
        }
        interface.do_express_checkout_payment(**kw)
        checkout_response = interface.get_express_checkout_details(token=kw['token'])
        pp_response = convert_pp_response_to_dict(checkout_response)
        if pp_response is None:
            abort(404)
        id_extra = None
        if pp_response.get('CHECKOUTSTATUS') == 'PaymentActionCompleted':
            uid = pp_response.get('UID_CUSTOMER')
            wrap = Wrapper()
            if uid is None:
                logging.info("PP RESPONSE don't have FIELD: PAYMENTREQUEST_0_CUSTOM and PAYMENTREQUEST_0_INVNUM")
                abort(404)
            if uid is not None:
                id_extra = GetIdExtraOrder(uid)
                if id_extra:
                    uid = uid.replace(MASK_EXTRAORDER.format(id_extra), "")
                else:
                    Orders().status_change(uid, 2, session['site_id'])
            else:
                tsm_mail_list = (str(SysConst().Get_Sys_Const("support_mail"))).split(',')
                for x in tsm_mail_list:
                    send_mail_from_server('[!] UID ERROR [!]', x, '', '[!] UID ERROR [!]')
            order_id = Orders().get_id_by_uid(uid, session['site_id'])[0].get('id')
            CurentDate = time.strftime("%Y-%m-%d %H:%M:%S")
            id_customer = session.get('id', None) or Orders().get_customer_id_by_uid(uid)[0].get('id_customer')
            id_transaction = pp_response.get('TRANSACTIONID_CUSTOMER')
            if id_transaction is None:
                logging.info("PP RESPONSE don't have FIELD: PAYMENTREQUESTINFO_0_TRANSACTIONID and " +
                             "PAYMENTREQUEST_0_TRANSACTIONID and TRANSACTIONID")
                abort(404)
            id_trans = Transactions().add_transactions(pp_response.get('EMAIL'),
                                                       html_escape(pp_response.get('FIRSTNAME')),
                                                       html_escape(pp_response.get('LASTNAME')),
                                                       CurentDate,
                                                       pp_response.get('TOKEN'), pp_response.get('PAYERID'),
                                                       pp_response.get('COUNTRYCODE'),
                                                       pp_response.get('CHECKOUTSTATUS'),
                                                       order_id, id_customer, id_transaction)
            if id_extra:
                logging.info('[i] EXTRA UID:{0}'.format(id_extra))
                wrap = Wrapper()
                CurentDate = time.strftime("%Y-%m-%d %H:%M:%S")
                Date = datetime.datetime.strptime(CurentDate, "%Y-%m-%d %H:%M:%S")
                Extraorders(wrap).add_trans_id({"id_transaction": id_trans, "date_paid": Date}, id_extra)
                Extraorders(wrap).assign_extraorder(id_extra)
                X_TOKEN_SYSTEM = str(SysConst().Get_Sys_Const("auth_token_system"))
                SendRequestToSystem(1, url1=URL_SYSTEM, data1=id_extra, data2=order_id, header1=X_TOKEN_SYSTEM,
                                    id_customer=id_customer)
                Events().add_event(str(id_extra) + " extraorder has been paid by user " + str(id_customer),
                                   81, order_id, id_customer)
            else:
                Events().add_event(str(order_id) + " has been paid by user " + str(id_customer),
                                   2, order_id, id_customer)
            Customer().send_mail_to_client_payment(order_id)
            if id_extra:
                Customer().send_mail_to_support_payment(order_id, id_extra)
            else:
                Customer().send_mail_to_support_payment(order_id)
            # smstext = Orders().get_order_to_sms(order_id)
            tsm_mail_list = (str(SysConst().Get_Sys_Const("support_mail"))).split(',')
            if id_extra:
                uid = "{0}_{1}".format(uid, id_extra)
            for x in tsm_mail_list:
                send_mail_from_server('{0} Order Paid:'.format(ShortSiteName(site_name)), x, '',
                                      'Order: {0}<br> User: {1}'.format(uid, id_customer))
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('dashboard'))
    except Exception as e:
        logging.info('[e] Exception /paypal/do/ :  {0}'.format(e))
        logging.exception('[e] Exception /paypal/do/ :  {0}'.format(e))
        err = str(e)
        if err:
            if err.find('Error Code:') >= 0:
                ppec = -1
                try:
                    ppec = str(err[err.find('Error Code:'):].replace(')', '').replace('Error Code:', '')).strip()
                except Exception as e:
                    return redirect(url_for('dashboard', ppec=str(ppec)))
                return redirect(url_for('dashboard', ppec=str(ppec)))
        logging.info('[e] PayPal ERROR = {0}'.format(err))
        return redirect(url_for('dashboard', ppec='-1'))


@app.route("/paypal/cancel")
def paypal_cancel():
    return redirect(url_for('dashboard'))



# ----------------------------------------------------------------------------
@app.route('/alogin', methods=['POST'])
def alogin():
    if request.method == 'POST':
        result = {}
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        if Users().api_login({"email": result.get("email"), "password": result.get("password")}, result.get("site_id")):
            id_user = Users().get_customer_id(escape(result.get("email")), escape(result.get("site_id")))
            data = {}
            data['id'] = id_user[0].get('id')
            data['logged_in'] = True
            data['site_id'] = result.get("site_id")
            session['id'] = id_user[0].get('id')
            session['site_id'] = result.get("site_id")
            session['logged_in'] = True
            update_data(session['site_id'])
            return redirect(url_for('dashboard'))
        else:
            return '1'


@app.route('/aregistration', methods=['POST'])
def aregistration():
    if request.method == 'POST':
        result = {}
        f = request.form
        email = ""
        password = ""
        site_id = 35
        fname = "-"
        lname = "-"
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        if (result.get('fr') == "1"):
            characters = string.ascii_letters + string.digits
            password_chr = "".join(random.choice(characters) for x in range(randint(8, 10)))
            email = escape(result.get('email'))
            phone = escape(result.get('phone'))
            site_id = escape(result.get('site_id'))
            password = escape(password_chr)
            cpassword = escape(password_chr)
        else:
            if (len(str(escape(result.get('fname')))) > 0):
                fname = escape(result.get('fname'))
            if (len(str(escape(result.get('lname')))) > 0):
                lname = escape(result.get('lname'))
            email = escape(result.get('email'))
            phone = escape(result.get('phone'))
            site_id = escape(result.get('site_id'))
            password = escape(result.get('password'))
            cpassword = escape(result.get('cpassword'))
        id_user = Users().aregistration(fname, lname, email, phone, password, site_id)
        data = {}
        data['id'] = id_user
        data['logged_in'] = True
        data['site_id'] = site_id
        update_data(site_id)
        if (fname == "-"):
            # ##logging.info('[i] INFO send registration mail on = {0}'.format( email) )
            fname = "Client"
            lname = ""
            # ##send_mail(site_mail,site_pass,site_mail,email,"Password to {0}!".format(site_name),"","Hello! Your password is <b>{0}</b>. <br> Please add <i>last name & first name</i> on profile. <br> You can change the password in profile.".format(password))
        if id_user is not None:
            session['id'] = id_user
            session['logged_in'] = True
            Events().add_event_no_order("A new client has registered. ID#" + str(id_user) + " has been assigned", 37,
                                        id_user)
            # ##logging.info('fname = {0}'.format(fname))
            site_name = "name"
            site_name_short = "name"
            msg = "Hello, dear <i>{0}</i>,<br>".format(fname.lower().title()) + \
                  "You have successfully registered at <i>{0}</i>.<br>".format(site_name_short) + \
                  "Your login credentials are as follows:<br>" + \
                  "<b>Email</b>: {0}<br>".format(email) + \
                  "<b>Password</b>: {0}<br>".format(password) + \
                  "Should you have any questions or concerns do not hesitate to contact us at <u>{0}</u> or live chat.<br>".format(
                      site_mail) + \
                  "Kind regards<br><hr>" + \
                  "{0} support team<br>".format(site_name_short) + \
                  "{0}".format(site_mail)
            send_mail(site_mail, site_pass, "{0} <{1}>".format(ShortSiteName(site_name), site_mail), email,
                      "You've signed up at {0}!".format(site_name_short), "", msg)
            return json.dumps(data)
        else:
            return '1'


@app.route('/checkmail', methods=['POST'])
@cross_origin(supports_credentials=True)
def checkmail():
    if request.method == 'POST':
        result = {}
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        mail = escape(result.get('email'))
        site_id = escape(result.get('site_id'))
        if (Users().is_email_exist(mail, site_id)[0].get("count(email)") == 0):
            return '0'
        else:
            return '1'


# ----------------------------------------------------------------------------


@app.route('/checkdiscount', methods=['POST'])
def checkdiscount():
    if request.method == 'POST':
        result = {}
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        discountcode = escape(result.get('discountcode'))
        disc = Orders().get_discount(discountcode)
        if (disc > 0):
            return str(disc)
        else:
            return str(0)


# ----------------------------------------------------------------------------


@app.route('/getdiscount', methods=['POST'])
def getdiscount():
    if request.method == 'POST':
        result = {}
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        customer_mail = escape(result.get('mail'))
        send_mail(site_mail, site_pass, "{0} <{1}>".format(ShortSiteName(site_name), site_mail), customer_mail,
                  "Discount Code!", "", "Here is your personal 10% OFF discount code: OFF10PD")
        return str('0')


# Topic: Discount Code!
# Text: Here is your personal 10% OFF discount code: OFF10PD
# ----------------------------------------------------------------------------


@app.route('/contactus', methods=['POST'])
def contactus():
    if request.method == 'POST':
        result = {}
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        id_frm = escape(result.get('id_frm'))
        name = result.get('name')
        email = escape(result.get('email'))
        message = result.get('message')
        if (id_frm == "0"):
            phone = result.get('phone', None)
            Customer().send_mail_to_support_from_contactform(name, email, message, phone)
        elif (id_frm == "1"):
            send_mail(site_mail,
                      site_pass,
                      "{0} <{1}>".format(ShortSiteName(site_name), site_mail),
                      SysConst(APP_ROOT).Get_Sys_Const("recruiting_tsm_mail_address"),
                      "New writer application from {0}".format(site_name),
                      "",
                      "<b>New writer application</b> from {0} <br><b>First name:</b> {1}<br><b>Email:</b> {2}".format(
                          site_name, name, email)
                      )
    return "0"


@app.route('/my_orders')
@login_required
def myorders():
    page_url = "'/my_orders.html','/my_orders'"
    list_contents = SysConst(APP_ROOT).GetHTML_Content_Pages(page_url.lower())
    list_contents_include = SysConst(APP_ROOT).GetHTML_Include_Content_Pages()
    template_pages = SysConst(APP_ROOT).Get_Template_Pages(page_url.lower())
    orderslist = Orders().get_odresrsbyuser(session['id'])
    return render_template(template_pages,
                           list_contents=list_contents,
                           list_contents_include=list_contents_include,
                           orderslist=orderslist)


@app.route('/my_orders/')
def myorders2():
    return redirect(url_for('myorders'))


@app.route('/transactions')
@login_required
def transactions():
    page_url = "'/transactions.html','/transactions'"
    list_contents = SysConst(APP_ROOT).GetHTML_Content_Pages(page_url.lower())
    list_contents_include = SysConst(APP_ROOT).GetHTML_Include_Content_Pages()
    template_pages = SysConst(APP_ROOT).Get_Template_Pages(page_url.lower())
    transactions = Transactions().get_transactions(session['id'])
    return render_template(template_pages,
                           list_contents=list_contents,
                           list_contents_include=list_contents_include,
                           transactions=transactions)


@app.route('/transactions/')
def transactions2():
    return redirect(url_for('transactions'))


@app.route('/profile')
@login_required
def profile():
    page_url = "'/profile.html','/profile'"
    list_contents = SysConst(APP_ROOT).GetHTML_Content_Pages(page_url.lower())
    list_contents_include = SysConst(APP_ROOT).GetHTML_Include_Content_Pages()
    template_pages = SysConst(APP_ROOT).Get_Template_Pages(page_url.lower())
    site = str(SysConst().Get_Sys_Const("site_name"))
    site_short = ShortSiteName(site_name)
    customer_info = Customer().get_customer_info(session['id'], session['site_id'])
    return render_template(template_pages,
                           list_contents=list_contents,
                           list_contents_include=list_contents_include,
                           customer=customer_info,
                           site_short=site_short,
                           site=site)


@app.route('/profile/')
def profile2():
    return redirect(url_for('profile'))


@app.route('/dashboard', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required
def dashboard():
    page_url = "'/dashboard.html','/dashboard'"
    list_contents = SysConst(APP_ROOT).GetHTML_Content_Pages(page_url.lower())
    list_contents_include = SysConst(APP_ROOT).GetHTML_Include_Content_Pages()
    template_pages = SysConst(APP_ROOT).Get_Template_Pages(page_url.lower())
    site_id = session['site_id']
    user_id = session['id']

    orderslist = Orders().get_odresrsbyuser(user_id, site_id)
    fileslistorder = Orders().get_list_file_by_order(session['id'], session['site_id'])
    fileslist = Dashboard().get_new_files(session['id'])
    newmessage = Dashboard().get_new_messages(session['id'])
    # ##logging.info("orderslist = {0}".format(orderslist))
    # ##for orders in orderslist:
    # ##    logging.info("orders = {0}".format(orders))
    return render_template(template_pages,
                           list_contents=list_contents,
                           list_contents_include=list_contents_include,
                           orderslist=reversed(orderslist),
                           newmessages=newmessage,
                           files=fileslist,
                           fileslistorder=fileslistorder)


@app.route('/dashboard/', methods=['GET'])
def dashboard2():
    return redirect(url_for('dashboard'))


@app.route('/orderinfo', methods=['GET'])
@login_required
def orderinfo():
    user_id =  session['id']
    site_id =  session['site_id']

    page_url = "'/orderinfo.html','/orderinfo'"
    list_contents = SysConst(APP_ROOT).GetHTML_Content_Pages(page_url.lower())
    list_contents_include = SysConst(APP_ROOT).GetHTML_Include_Content_Pages()
    template_pages = SysConst(APP_ROOT).Get_Template_Pages(page_url.lower())

    uid = escape(request.args.get('id'))

    id_order = Orders().get_id_by_uid(uid, session['site_id'])[0]['id']

    userorders = list(Orders().get_all_ordersid_byuser(session['id'], session['site_id']))
    customer_email = str(Customer().get_customer_info(session['id'], session['site_id'])).lower()

    xx = [int(x['id']) for x in userorders]
    if int(id_order) in xx:
        orderslist = Orders().get_full_order(id_order, session['site_id'])
        allfiles = Orders().get_all_files(id_order)
        cfiles = Orders().get_all_customer_files(id_order)
        wfiles = Orders().get_all_writers_files(id_order)
        allmsg = Messages().get_all_message(id_order)
        rev_categ = Revisions().get_revison_categories()
        rev_levels = Revisions().get_revison_levels()
        # ##logging.info("rev_categ = {0}".format(rev_categ))
        # ##logging.info("rev_levels = {0}".format(rev_levels))

        wrap = Wrapper()
        subjects = Subject(wrap).get_list_active_subj()
        orderassign = OrderAssignment(wrap).get_list_active_orderassign()

        return render_template(template_pages,
                               list_contents=list_contents,
                               list_contents_include=list_contents_include,
                               orderslist=orderslist,
                               files=allfiles,
                               cfiles=cfiles,
                               wfiles=wfiles,
                               messages=allmsg,
                               customer_email=customer_email,
                               rev_levels=rev_levels,
                               rev_categ=rev_categ,
                               subjects=subjects,
                               orderassign=orderassign
                               )
    else:
        abort(404)


@app.route('/orderinfo/', methods=['GET'])
def orderinfo2():
    return redirect(url_for('orderinfo'))


@app.route('/forgot', methods=['GET'])
def forgot():
    page_url = "'/forgot.html','/forgot'"
    list_contents = SysConst(APP_ROOT).GetHTML_Content_Pages(page_url)
    list_contents_include = SysConst(APP_ROOT).GetHTML_Include_Content_Pages()
    template_pages = SysConst(APP_ROOT).Get_Template_Pages(page_url)
    return render_template(template_pages,
                           list_contents=list_contents,
                           site_mail=site_mail,
                           list_contents_include=list_contents_include)

@app.route('/forgot.html', methods=['GET', 'POST'])
def forgot3():
    return redirect(url_for('forgot'))


@app.route('/forgotpassword', methods=['POST'])
def reset_password():
    customer_email = escape(request.form.get('mail'))
    if customer_email:
        if Customer().reset_password(customer_email):
            return "0"
        else:
            return "1"


@app.route('/logout')
@cross_origin(supports_credentials=True)
def logout():
    session.pop('id', None)
    session.pop('role', None)
    session.pop('logged_in', None)
    session.clear()
    return "You are successfully logged out" 


@app.route('/logout/')
def logout2():
    return redirect(url_for('logout'))


@app.route('/sendmessages', methods=['POST'])
@login_required
def sendmessages():
    """
        Send message from form ORDERINFO
        Logout from system
        Andrey Krupenya
        
        UPD: 24 02 2016
            ADD: Check - is the order paid (return 3, order_status>1) or not paid (return 0, order_status<=1)
    """
    if request.method == 'POST':
        result = {}
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        message = escape(result.get("bodymessage"))
        old_message = result.get("bodymessage")
        orderid = escape(result.get("orderid"))
        subject = escape(result.get("subject", None))

        # ##logging.info("Messages send_subject subject = {0}; orderid = {1};".format(subject, orderid))

        id_order = Orders().get_id_by_uid(orderid)[0].get('id')
        # ##logging.info("ID {0}".format(Orders().get_id_by_uid(orderid)[0].get('id')))

        # ##id_order = orderid
        order_status = Orders().get_full_order(id_order)[0].get('id_order_status')
        order_status = int(order_status)
        # ##logging.info("1 order_status = {0}".format(order_status))
        if order_status > 1:
            # ##logging.info("2 order_status = {0}".format(order_status))
            curdatetime = time.strftime("%Y-%m-%d %H:%M:%S")
            customerid = session['id']
            id_subject = Messages().send_subject(subject, id_order)
            Messages().send_message_nofile(curdatetime, id_subject, message, customerid)
            # ##logging.info(Customer().get_customer_info(customerid)[0].get('email'))
            email_customer = str(Customer().get_customer_info(customerid)[0].get('email'))
            first_name = str(Customer().get_customer_info(customerid)[0].get('first_name'))
            last_name = str(Customer().get_customer_info(customerid)[0].get('last_name'))
            # ##logging.info("Messages Subject = {0}; Message = {1}; Costumer E-mail = {2}; Order ID: = {3};".format(subject, message, email_writer, orderid))
            site_name = str(SysConst().Get_Sys_Const("site_name"))
            site_name_short = str(site_name).replace('http', '').replace('https', '').replace(':', '').replace('/', '')
            msg = "Subject: <u>{0}</u><br>".format(subject) + \
                  "Message: {0}<br>".format(old_message) + \
                  "First Name: <i>{0}</i><br>".format(first_name) + \
                  "Customer email: <i>{0}</i><br>".format(email_customer) + \
                  "Order ID: <i>{0}</i><br>".format(orderid)
            send_mail(site_noreply_mail, site_noreply_pass, site_noreply_mail, site_mail,
                      "Dashbaord message from {0}".format(site_name_short), "", msg)
            # ##send_mail(site_noreply_mail, site_noreply_pass, site_noreply_mail, site_mail,subject,"","Time send message: {0} ;<br/> Subject: {1} ;<br> Message: {2} ;<br/> First name costumer: <b>{3}</b>;<br/> Last name costumer: <b>{4}</b>;<br/> Costumer E-mail: <i>{5}</i> ;<br/> Order ID: <b>{6}</b>".format(curdatetime, subject, old_message, first_name, last_name, email_writer, orderid))
            return "3"

    return "0"


@app.route('/updateprofile', methods=['POST'])
@login_required
def updateprofile():
    if request.method == 'POST':
        result = {}
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        name = escape(result.get("name"))
        phone = escape(result.get("phone"))
        email = escape(result.get("email"))
        newsletters = escape(result.get("newsletters"))
        Customer().customer_profile_update(session['id'], name, phone, '', email, newsletters)
    return "0"


@app.route('/updatepassword', methods=['POST'])
@login_required
def updatepassword():
    result = {}
    f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            result[key] = value
    old = escape(result.get("password"))
    new = escape(result.get("newpass"))
    if Customer().customer_password_update(session['id'], old, new) == "ok":
        return "0"
    # ##logging.info("UPD pass {0}".format(str(Customer().customer_password_update(session['id'], old, new))))
    return "1"


# Order form Start
@app.route('/order', methods=['POST'])
def order():
    page_url = "'/orderform.html','/orderform','/order.html','/order'"
    list_contents = SysConst(APP_ROOT).GetHTML_Content_Pages(page_url)
    list_contents_include = SysConst(APP_ROOT).GetHTML_Include_Content_Pages()
    template_pages = SysConst(APP_ROOT).Get_Template_Pages(page_url)

    def_val_academ_level = str(SysConst(APP_ROOT).Get_Sys_Const("def_val_academ_level"))
    def_val_paper_format = str(SysConst(APP_ROOT).Get_Sys_Const("def_val_paper_format"))
    add_days_to_deadline = str(SysConst(APP_ROOT).Get_Sys_Const("add_days_to_deadline"))
    add_def_placeholder_title = str(SysConst(APP_ROOT).Get_Sys_Const("add_def_placeholder_title"))
    add_def_placeholder_paper_details = str(SysConst(APP_ROOT).Get_Sys_Const("add_def_placeholder_paper_details"))

    fb_appId = str(SysConst(APP_ROOT).Get_Sys_Const("fb_appId"))
    tw_oauth_consumer_key = str(SysConst(APP_ROOT).Get_Sys_Const("oauth_consumer_key"))
    tw_oauth_nonce = str(SysConst(APP_ROOT).Get_Sys_Const("oauth_nonce"))
    tw_oauth_signature = str(SysConst(APP_ROOT).Get_Sys_Const("oauth_signature"))
    tw_oauth_signature_method = str(SysConst(APP_ROOT).Get_Sys_Const("oauth_signature_method"))
    tw_oauth_timestamp = str(SysConst(APP_ROOT).Get_Sys_Const("oauth_timestamp"))
    tw_oauth_token = str(SysConst(APP_ROOT).Get_Sys_Const("oauth_token"))
    show_other_registration = str(SysConst(APP_ROOT).Get_Sys_Const("show_other_registration"))
    google_token = str(SysConst(APP_ROOT).Get_Sys_Const("google_token"))

    wrap = Wrapper()
    subjects = Subject(wrap).get_list_active_subj()
    orderassign = OrderAssignment(wrap).get_list_active_orderassign()

    if request.method == 'POST':
        result = {}
        quote = ""
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        academicLevel = escape(result.get('academicLevel'))
        papertype = escape(result.get('paperType'))
        pages = escape(result.get('pages'))
        deadline = escape(result.get('deadline'))
        if (not result.get('quote') is None):
            quote = escape(result.get('quote'))
            if (result.get('quote') == ""):
                quote = "Writer's choice"
        return render_template(template_pages,
                               academicLevel=academicLevel,
                               papertype=papertype,
                               pages=pages,
                               deadline=deadline,
                               quote=quote,
                               def_val_academ_level=def_val_academ_level,
                               def_val_paper_format=def_val_paper_format,
                               add_days_to_deadline=add_days_to_deadline,
                               add_def_placeholder_title=add_def_placeholder_title,
                               add_def_placeholder_paper_details=add_def_placeholder_paper_details,
                               fb_appId=fb_appId,
                               tw_oauth_consumer_key=tw_oauth_consumer_key,
                               tw_oauth_nonce=tw_oauth_nonce,
                               tw_oauth_signature=tw_oauth_signature,
                               tw_oauth_signature_method=tw_oauth_signature_method,
                               tw_oauth_timestamp=tw_oauth_timestamp,
                               tw_oauth_token=tw_oauth_token,
                               show_other_registration=show_other_registration,
                               google_token=google_token,
                               subjects=subjects,
                               orderassign=orderassign,
                               list_contents=list_contents,
                               list_contents_include=list_contents_include

                               )
    if request.method == 'GET':
        deadline = request.args.get('tm')
        if (deadline):
            if (float(deadline) < 1):
                deadline = time.strftime("%Y-%m-%d")
        return render_template(template_pages,
                               deadline=deadline,
                               def_val_academ_level=def_val_academ_level,
                               def_val_paper_format=def_val_paper_format,
                               add_days_to_deadline=add_days_to_deadline,
                               add_def_placeholder_title=add_def_placeholder_title,
                               add_def_placeholder_paper_details=add_def_placeholder_paper_details,
                               fb_appId=fb_appId,
                               tw_oauth_consumer_key=tw_oauth_consumer_key,
                               tw_oauth_nonce=tw_oauth_nonce,
                               tw_oauth_signature=tw_oauth_signature,
                               tw_oauth_signature_method=tw_oauth_signature_method,
                               tw_oauth_timestamp=tw_oauth_timestamp,
                               tw_oauth_token=tw_oauth_token,
                               show_other_registration=show_other_registration,
                               google_token=google_token,
                               subjects=subjects,
                               orderassign=orderassign,
                               list_contents=list_contents,
                               list_contents_include=list_contents_include
                               )


@app.route('/orderform/', methods=['GET', 'POST'])
def order2():
    return redirect(url_for('order'))


@app.route('/orderform.html', methods=['GET', 'POST'])
def order3():
    return redirect(url_for('order'))


@app.route('/order/', methods=['GET', 'POST'])
def order4():
    return redirect(url_for('order'))


@app.route('/orderform', methods=['GET', 'POST'])
def order5():
    return redirect(url_for('order'))


@app.route('/order.html', methods=['GET', 'POST'])
def order6():
    return redirect(url_for('order'))


@app.route('/make_order', methods=['POST'])
@cross_origin(supports_credentials=True)
def makeorder():
    logging.info('[i] Make new ORDER!')
    if request.method == 'POST':
        result = {}
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        logging.info(" 0 deadlineDate = {0}".format(result.get('deadlineDate')))
        workType = escape(result.get('workType'))
        academic_levels = escape(result.get('academicLevel'))
        paper_format = escape(result.get('paperFormat'))
        assigment = escape(result.get('paperType'))
        subject = escape(result.get('subject'))
        topic = escape(html_escape(result.get('topic').encode("utf-8"), 0))
        # ##topic = result.get('topic').encode("utf-8")
        paper_details = escape(html_escape(result.get('paperDetails').encode("utf-8"), 0))
        # ##paper_details = result.get('paperDetails').encode("utf-8")
        page = escape(result.get('pages'))
        source = escape(result.get('sources'))

        spaced = escape(result.get('spaced'))
        deadlineDate = escape(result.get('deadlineDate'))
        discount = escape(result.get('discount'))
        curdate = time.strftime("%Y-%m-%d")
        xhoures = escape(result.get('xhoures'))
        customerid = escape(result.get('user_id'))
        files = request.files.getlist('file[]')

        site_id = escape(result.get('site_id'))

        curdatetime = time.strftime("%Y-%m-%d %H:%M:%S")
        CurentDate = time.strftime("%Y-%m-%d %H:%M:%S")
        Date = datetime.datetime.strptime(CurentDate, "%Y-%m-%d %H:%M:%S")
        Deadline = Date
        wr_deadline = Date

        if not deadlineDate:
            xhoures = '12'
        if xhoures == '12':
            urgency = '0.12'
        else:
            urgency = delta_date(deadlineDate, curdate)

        if urgency == 0:
            urgency = '0.12'

        price = 0

        workType2 = 1
        if workType == "1":
            workType2 = 2
        elif workType == "3":
            workType2 = 3
            spaced = 2
        dd = GetUrgency(deadlineDate)
        if (dd > 0):
            urgency = dd
            # ##logging.info("deadlineDate = {0}".format(result.get('deadlineDate')))
            # ##logging.info("xhoures = {0}".format(result.get('xhoures')))
            price = GetCurentPriceForWork(workType2, int(academic_levels), dd, spaced, page, None)
            # ##logging.info("price = {0}".format(price))
            # ##logging.info("workType2 = {0}".format(workType2))
            # ##logging.info("academic_levels = {0}".format(academic_levels))
            # ##logging.info("dd = {0}".format(dd))
            # ##logging.info("spaced = {0}".format(spaced))
            # ##logging.info("page = {0}".format(page))

            discount_persent = 0
        basic_price = price
        if (discount):
            discount_persent = Orders().get_discount(discount)
            if (int(discount_persent) > 0):
                price = round(price - (price * (float(discount_persent) / 100)), 2)

        # -- Deadline --
        if (urgency == '0.12'):
            # Deadline = Date + datetime.timedelta(hours=12)
            Deadline = datetime.datetime.strptime(deadlineDate, "%Y-%m-%d") + datetime.timedelta(hours=12)
            wr_deadline = Date + datetime.timedelta(hours=12 * 0.75)
        else:
            if (int(urgency) == 0):
                # Deadline = Date + datetime.timedelta(hours=12)
                Deadline = datetime.datetime.strptime(deadlineDate, "%Y-%m-%d") + datetime.timedelta(hours=12)
                wr_deadline = Date + datetime.timedelta(hours=12 * 0.75)
            if (int(urgency) >= 1):
                # Deadline = Date + datetime.timedelta(days=int(urgency))
                Deadline = datetime.datetime.strptime(deadlineDate, "%Y-%m-%d") + datetime.timedelta(hours=12)
                wr_deadline = Date + datetime.timedelta(days=int(urgency) * 0.75)
        # -- End Deadline --

        # -- Generate UID --
        wrap = Wrapper()
        uid = OrderAssignment(wrap).get_asign_prefix(int(assigment))[0].get('prefix')
        if uid is None:
            uid = 'NN-'
        uid = uid + str(datetime.datetime.now().strftime('%y%m%d%H%M%S'))
        # -- End UID Generate --

        rr = ''
        if urgency == '0.12' or int(urgency) == 0:
            rr = Orders().get_order_rating(1, int(page), 0.5)
        else:
            rr = Orders().get_order_rating(1, int(page), int(urgency))

        lastid = Orders().addorder(
            {"id_site": site_id, "uid": uid, "price": price, "date": curdatetime, "deadline": Deadline, "pages": page,
             "sources": source, "paper_format": paper_format, "language": "en", "topic": topic,
             "id_academic_level": academic_levels, "urgency": urgency, "paper_details": paper_details, "comment": "",
             "discount": discount_persent, "discount_code": discount, "plagiarism_status": 1, "id_customer": customerid,
             "id_order_status": 1, "id_assignment": assigment, "id_subject": subject, "features": "", "country": "",
             "rr": rr, "wr_deadline": wr_deadline, "type_work": workType, "spaced": spaced, "basic_price": basic_price})

        # ## FIX for lastid=-1 for some orders (29 03 2016)
        # ## Upd 11 04 2016
        if lastid < 0:
            logging.info(
                '[i] Order UID (SOME ERROR on inser to ORDERS table): {0} Price: {1} Deadline: {2} Lastid: {3}'.format(
                    uid, price, Deadline, lastid))
            lastid = Orders().get_id_by_uid(uid, session['site_id'])
            logging.info('[i] Order ID Update - Lastid: {0}'.format(lastid))
        # ## END FIX

        for file in files:
            hash = hashlib.sha1()
            hash.update(str(time.time()))
            if file and allowed_file(file.filename):
                realname = escape(file.filename)
                filename = escape(hash.hexdigest()[:12] + secure_filename(file.filename))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                Files().addfile(
                    {"name": realname, "path": filename, "id_order": lastid, "id_customer": str(result.get('user_id')),
                     "date": curdatetime})

        Events().add_event(escape("Order " + str(lastid) + " has been created by user " + str(result.get('user_id'))), 1,
                           lastid, result.get('user_id'))
        try:
            send_mail_to_support(lastid, price)  # mail to support
        except Exception, e:
            logging.info('[e] ERROR ON - Csend_mail_to_support(*)')
            logging.info('[i] send_mail_to_support: {0}'.format(e))
        else:
            pass
        finally:
            pass
        try:
            Customer().send_mail_to_client(lastid)  # mail to client
        except Exception, e:
            logging.info('[e] ERROR ON - Customer().send_mail_to_client(*)')
            logging.info('[i] send_mail_to_client(lastid) - Lastid: {0}'.format(lastid))
            logging.info(
                '[i] RESULT send_mail_to_client(lastid) = {0}'.format(Customer().get_customer_info_by_order(lastid, session['site_id'])))
        else:
            pass
        finally:
            pass
    logging.info('[i] Order UID: {0} Price: {1} Deadline: {2} Lastid: {3}'.format(uid, price, Deadline, lastid))
    logging.info(
        '[i] Orders parameters: WorkType: {0} academicLevel {1} pages {2} spaced {3}'.format(workType2, academic_levels,
                                                                                             page, spaced))
    return redirect(url_for('dashboard', orderid=uid, _external=True, _scheme='https'))
    #return redirect(url_for('dashboard', _external=True, _scheme='https'))


@app.route('/make_order/', methods=['POST'])
def makeorder2():
    return redirect(url_for('makeorder'))


@app.route('/calc_price', methods=['POST'])
def calc_price():
    auth_token = request.headers.get('X-Auth-Token')
    auth_token_local = str(SysConst(APP_ROOT).Get_Sys_Const("auth_token"))
    if auth_token == auth_token_local:
        urgency = escape(request.form.get("urgency", None))
        pages = escape(request.form.get("pages", None))
        id_academic_level = escape(request.form.get("id_academic_level", None))
        spaced = escape(request.form.get("spaced", None))
        type_of_work = escape(request.form.get("type_of_work", None))
        discount_code = escape(request.form.get("discount_code", None))

        if not (urgency and pages and id_academic_level and spaced and type_of_work):
            abort(404)
        if type_of_work == "1":
            type_of_work = 2
        elif type_of_work == "2":
            type_of_work = 1
        elif type_of_work == "3":
            type_of_work = 3

        try:
            basic_order_price = GetCurentPriceForWork(
                type_of_work,
                id_academic_level,
                urgency,
                spaced,
                pages,
                None
            )
            final_order_price = GetCurentPriceForWork(
                type_of_work,
                id_academic_level,
                urgency,
                spaced,
                pages,
                discount_code
            )
            data = json.dumps({'basic_order_price': basic_order_price,
                               'final_order_price': final_order_price})
            return Response(data, status=201)
        except Exception, e:
            logging.info("ERROR on route calc_price : {0}".format(e))
            return Response(status=404)
    return Response(status=404)


# Work with file start
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        result = {}
        f = request.form
        # ##logging.info("request.form= {0}".format(f))
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        lastid = escape(result.get("orderid"))
        files = request.files.getlist('file')
        # ##logging.info("request.files= {0}".format(request.files))
        curdatetime = time.strftime("%Y-%m-%d %H:%M:%S")

        if (not request.form.get('ajax_loader_file') is None):
            files = request.files.getlist('file')
            # ##logging.info("files= {0}".format(files))
            for file in files:
                hash = hashlib.sha1()
                hash.update(str(time.time()))
                if file and allowed_file(file.filename):
                    filenameold = escape(secure_filename(file.filename))
                    filename = escape(hash.hexdigest()[:12] + secure_filename(file.filename))
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    ftype = magic.from_file(os.path.join(app.config['UPLOAD_FOLDER'], filename)).lower()
                    # ##logging.info("addfile = {0}".format({"name":filenameold, "path":filename, "id_order":lastid, "id_customer":str(session['id']), "date":curdatetime}))
                    Files().addfile(
                        {"name": filenameold, "path": filename, "id_order": lastid, "id_customer": str(result.get('user_id')),
                         "date": curdatetime})
                else:
                    return jsonify(result="bad")
            if (not lastid is None):
                cfiles = Orders().get_all_customer_files(lastid)
                wfiles = Orders().get_all_writers_files(lastid)
                # ##logging.info("order_id= {0}".format(lastid))
                # ##logging.info(cfiles)
                # ##logging.info(wfiles)
                return jsonify(cfiles=cfiles, wfiles=wfiles)

            return jsonify(result="good")

        else:

            # ##logging.info("files = {0}".format(files))
            for file in files:
                hash = hashlib.sha1()
                hash.update(str(time.time()))
                if file and allowed_file(file.filename):
                    filenameold = escape(secure_filename(file.filename))
                    filename = escape(hash.hexdigest()[:12] + secure_filename(file.filename))
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    ftype = magic.from_file(os.path.join(app.config['UPLOAD_FOLDER'], filename)).lower()
                    # ##logging.info("addfile = {0}".format({"name":filenameold, "path":filename, "id_order":lastid, "id_customer":str(session['id']), "date":curdatetime}))
                    Files().addfile(
                        {"name": filenameold, "path": filename, "id_order": lastid, "id_customer": str(result.get('user_id')),
                         "date": curdatetime})
                else:
                    return "error"
    return redirect(url_for('dashboard'))


@app.route('/download', methods=['GET'])
def download_file():
    return send_file(DOWNLOAD_FOLDER + "/" + request.args.get('file'), attachment_filename=request.args.get('name'),
                     as_attachment=True)


@app.route('/download_customer', methods=['GET'])
def download_customer_file():
    return send_file(UPLOAD_FOLDER + "/" + request.args.get('file'), attachment_filename=request.args.get('name'),
                     as_attachment=True)


@app.route('/remoteupload', methods=['POST'])
@crossdomain(origin='*')
def remoteupload():
    password = escape(request.form.get("password", None))
    if password == 'remotepwd':
        files = request.files.getlist('file[]')
        uid = escape(request.form.get("uid", None))
        curdatetime = time.strftime("%Y-%m-%d %H:%M:%S")
        idorder = Orders().get_id_by_uid(uid, session['site_id'])[0].get('id')
        for file in files:
            if file:
                hash = hashlib.sha1()
                hash.update(str(time.time()))
                filename = hash.hexdigest()[:12] + escape(secure_filename(file.filename))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                id_rec_file = str(Files().addremotefile(
                    {"name": file.filename, "path": filename, "id_order": idorder, "id_writer": 1, "status": 0,
                     "date": curdatetime}))
                data = json.dumps(
                    {'fid': id_rec_file, 'name': file.filename, 'path': filename, 'date': str(curdatetime)})
                return Response(data, status=201)
            else:
                return Response(status=204)
    return Response(status=204)


@app.route('/remoteupload_customer', methods=['POST'])
@crossdomain(origin='*')
def remoteupload_customer():
    password = request.form.get('password', None)
    if password == None or password != 'remotepwd':
        return Response(status=204)

    file = request.files.get('file', None)
    id_order = request.form.get('id', None)
    id_customer = request.form.get('cid', None)
    status = request.form.get('status', 0)
    id_revision = request.form.get('id_revision', None)

    if file and id_order and id_customer:
        curdatetime = time.strftime("%Y-%m-%d %H:%M:%S")
        hash = hashlib.sha1()
        hash.update(str(time.time()))
        encode_file_name = hash.hexdigest()[:12] + secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, encode_file_name))
        if id_revision:
            fid = Files().addfile({"name": file.filename,
                                   "path": encode_file_name,
                                   "date": curdatetime,
                                   "id_order": id_order,
                                   "id_customer": id_customer,
                                   "delflag": status,
                                   "id_revision": id_revision})
        else:
            fid = Files().addfile({"name": file.filename,
                                   "path": encode_file_name,
                                   "date": curdatetime,
                                   "id_order": id_order,
                                   "id_customer": id_customer,
                                   "delflag": status})
        data = json.dumps({'fid': fid,
                           'name': file.filename,
                           'path': encode_file_name,
                           'date': str(curdatetime)})
        return Response(data, status=201)

    return Response(status=204)


@app.route('/utils', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def utils():
    """This function for creating claim.
       This function for calc price
       This function for update file conected to order
       This function for update order
    autor:  Andrey Krupenya
    date:   09 12 2015
    last update: 13 12 2015

    last update: START 29 01 2016 function return JSON list prices for work

    last update: START 22 02 2016 function mark file_customer as delete

    last update: START 02 03 2016 function mark order as delete

    last update: START 15 03 2016 function get PayPal Error

    last update: START 04 04 2016 function selcat2. Remove first char if it is - ','
    """
    if request.method == 'POST':
        quest_inf = {}

        if request.form.getlist('selcat2') is not None:
            selcat2 = request.form.getlist('selcat2')
            if len(selcat2) > 0:
                selcat2 = request.form.getlist('selcat2')
                Sel_CAT = ""
                for selcat in selcat2:
                    if selcat:
                        Sel_CAT = "{0},{1}".format(Sel_CAT, escape(str(selcat).encode('utf-8').strip()))
                # ##logging.info("with , :{0}".format(quest_inf['Sel_CAT']))
                if len(Sel_CAT) > 0:
                    if Sel_CAT[0] == ',':
                        Sel_CAT = Sel_CAT[1:]
                # logging.info("with out , :{0}".format(Sel_CAT))
                list_categ = Revisions().get_revison_list_categories(Sel_CAT)
                Sel_CAT = "[{}]".format(Sel_CAT)
                quest_inf['categories'] = Sel_CAT
                # logging.info("list categ :{0}".format(list_categ))

                # ##quest_inf['Sel_CAT']=escape(request.form.getlist('selcat2').encode('utf-8').strip())
                # ##quest_inf['ORDER_ID'] = escape(request.form.get('idorder').encode('utf-8').strip())
                uid = escape(request.form.get('idorder').encode('utf-8').strip())
                expext = \
                    Revisions().get_revison_levels(escape(request.form.get('aftrerrevision').encode('utf-8').strip()))[
                        0].get('level')
                # logging.info("expext :{0}".format(expext))
                quest_inf['id_level'] = escape(request.form.get('aftrerrevision').encode('utf-8').strip())
                text_for_message = request.form.get('describeproblem').encode('utf-8').strip()
                quest_inf['description'] = escape(text_for_message)
                # ##quest_inf['DOC_URL']=""
                # ##quest_inf['DOC_NAME']=""
                quest_inf['id_customer'] = str(session['id'])
                quest_inf['date_created'] = datetime.datetime.now()
                quest_inf['deadline'] = datetime.datetime.now() + datetime.timedelta(hours=24)
                quest_inf['id_site'] = str(SysConst(APP_ROOT).Get_Sys_Const("site_id"))
                quest_inf['id_order'] = Orders().get_id_by_uid(uid, session['site_id'])[0].get('id')
                # ##logging.info(escape(request.form.getlist('selcat2[]').encode('utf-8').strip()))
                # ##logging.info(request.form.getlist('selcat2'))
                # ##logging.info(quest_inf)
                id_rev = Revisions().add_revisiov(quest_inf)
                customer_info = Customer().get_customer_info(session['id'])
                customer_email = ""
                customer_name = "Client"
                try:
                    customer_email = str(customer_info[0].get('email'))
                except Exception, e:
                    customer_email = ""

                try:
                    customer_name = str(customer_info[0].get('first_name'))
                    if str(customer_name).strip() == '-':
                        customer_name = "Client"
                except Exception, e:
                    pass

                DOC_URL = ""
                DOC_NAME = ""
                curdatetime = time.strftime("%Y-%m-%d %H:%M:%S")
                id_ord = quest_inf['id_order']
                files = request.files.getlist('inputfl[]')
                for fileload in files:
                    if fileload and allowed_file(fileload.filename):
                        filename = escape(secure_filename(fileload.filename))
                        m = hashlib.md5()
                        m.update(str(filename) + datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
                        maskfile = (fileload.filename).rsplit('.', 1)[1]
                        linktofile = os.path.join(UPLOAD_FOLDER, "revision_" + m.hexdigest() + "." + maskfile)
                        fileload.save(linktofile)
                        # ##quest_inf['DOC_URL']+="claim_"+m.hexdigest()+"."+maskfile+":"
                        # ##quest_inf['DOC_NAME']+=filename+":"
                        FILE_REVISION_SHOW = 1
                        Files().addfile({"name": filename, "path": ("revision_" + m.hexdigest() + "." + maskfile),
                                         "id_order": id_ord, "id_customer": str(session['id']), "date": curdatetime,
                                         "id_revision": id_rev, "delflag": FILE_REVISION_SHOW})
                        DOC_URL += "revision_" + m.hexdigest() + "." + maskfile + ":"
                        DOC_NAME += filename + ":"
                # ##logging.info(quest_inf['ORDER_ID'])
                # ##logging.info(Orders().get_writer_info_by_order(quest_inf['ORDER_ID']))
                email_writer = str(Orders().get_writer_info_by_order(uid)[0].get('email'))
                fl = Orders().get_writer_info_by_order(uid)[0].get('first_name')
                site = str(SysConst().Get_Sys_Const("site_name"))
                site_short = str(site).replace('http', '').replace('https', '').replace(':', '').replace('/', '')
                # ##" "+\
                # ##Orders().get_writer_info_by_order(quest_inf['ORDER_ID'])[0].get('last_name')
                if email_writer != "":
                    send_mail(site_mail_revisions, site_mail_revisions_pass, site_mail_revisions, email_writer,
                              "Revision request: {0}".format(uid),
                              "",
                              "Hello, <i>{0}</i>,<br>".format(str(fl).lower().title()) +
                              "The client requested revision for your order <i>{0}</i><br>".format(uid) +
                              "Category: <i>{0}</i><br>".format(str(list_categ).replace(",", ", ")) +
                              "Level: <i>{0}</i><br>".format(str(expext)) +
                              "Claim: {0}<br>".format(str(text_for_message)) +
                              "Please proceed to the revisions menu at your personal dashboard at <a href='http://writing-center.com'>http://writing-center.com</a>.<br>" +
                              "Kind regards<hr>",
                              str(DOC_URL),
                              str(DOC_NAME))
                    Events().add_event(escape(
                        "Revision request: {0} send to writer email {1} from site {2}".format(uid, email_writer,
                        site_short)), 80, id_ord, session['id'])

                send_mail(site_mail_revisions, site_mail_revisions_pass, site_mail_revisions, site_mail,
                          "Revision request: {0}".format(uid),
                          "",
                          "Category: <i>{0}</i><br>".format(str(list_categ).replace(",", ", ")) +
                          "Level: <i>{0}</i><br>".format(str(expext)) +
                          "Body: {0}<br>".format(str(text_for_message)) +
                          "First Name: <i>{0}</i><br>".format(customer_name.lower().title()) +
                          "Customer email: <i>{0}</i><br>".format(customer_email) +
                          "Order ID: <i>{0}</i><br>".format(uid),
                          str(DOC_URL),
                          str(DOC_NAME))
                Events().add_event(escape(
                    "Revision request: {0} send to support email {1} from site {2}".format(uid, site_mail, site_short)),
                    80, id_ord, session['id'])

                if customer_email != "":
                    send_mail(site_mail, site_pass, "{0} <{1}>".format(ShortSiteName(site_name), site_mail),
                              customer_email,
                              "Revision request: {0}".format(uid),
                              "",
                              "Hello, <i>{0}</i>,<br>".format(customer_name.lower().title()) +
                              "We have successfully received your revision request for your order <i>{0}</i><br>".format(
                                  uid) +
                              "Kindly be informed that we reserve up to 48 hours to process your revision request. At the same " +
                              "time, we always do our best to revise orders as soon as possible. <br>" +
                              "Revised paper will be emailed to you. A copy of it will also become available for download from " +
                              "your personal account page at <a href='{0}' target='_blank'>{1}dashboard</a> <br>".format(
                                  site, site.lower()) +
                              "Thank you for your cooperation.<br>" +
                              "Warm regards<hr>" +
                              "{0} support team<br>".format(site_short) +
                              "{0}".format(site_mail))
                    Events().add_event(escape(
                        "Revision request: {0} send to support email {1} from site {2}".format(uid, site_mail,
                        site_short)), 80, id_ord, session['id'])
                return jsonify(result="good")

        if request.form.get('updprice') is not None:
            # ##for rc in request.form:
            # ##logging.info("{0} = {1}".format(rc,request.form.get(rc)))
            urgency = GetUrgency(escape(request.form.get('deadlineDate')))

            # ##logging.info("workType = {0}".format(request.form.get('workType')))

            price_with_discount = GetCurentPriceForWork(
                escape(request.form.get('workType')),
                escape(request.form.get('academicLevel')),
                urgency,
                escape(request.form.get('spaced')),
                escape(request.form.get('pages')),
                escape(request.form.get('discount').encode('utf-8').strip())
            )
            # ##logging.info(price_with_discount)
            if (price_with_discount is None):
                price_with_discount = " Please check filelds..."
            return jsonify(price=str(price_with_discount))

        if request.form.get('_editorder') is not None:
            urgency = GetUrgency(escape(request.form.get('deadlineDate')))
            workType = 1
            if str(request.form.get('workType')) == "1":
                workType = 2
            elif str(request.form.get('workType')) == "3":
                workType = 3
            # ##logging.info("workType = {0}".format(request.form.get('workType')))
            # ##logging.info("new workType = {0}".format(workType))
            price_with_discount = GetCurentPriceForWork(
                escape(request.form.get('workType')),
                escape(request.form.get('academicLevel')),
                urgency,
                escape(request.form.get('spaced')),
                escape(request.form.get('pages')),
                escape(request.form.get('discount').encode('utf-8').strip())
            )
            if price_with_discount is not None:
                curdatetime = time.strftime("%Y-%m-%d %H:%M:%S")
                discount_persent = Orders().get_discount(escape(request.form.get('discount').encode('utf-8').strip()))
                # ##logging.info("_editorder : {0}".format(str(price_with_discount)))
                Orders().updorder({"price": price_with_discount, "urgency": urgency, "discount": discount_persent,
                                   "date": curdatetime, "deadline": escape(request.form.get('deadlineDate')),
                                   "pages": escape(request.form.get('pages')),
                                   "sources": escape(request.form.get('sources')),
                                   "paper_format": escape(request.form.get('paperFormat')),
                                   "topic": escape(request.form.get('topic').encode('utf-8').strip()),
                                   "id_academic_level": escape(request.form.get('academicLevel')),
                                   "paper_details": escape(request.form.get('paperDetails').encode('utf-8').strip()),
                                   "discount_code": escape(request.form.get('discount').encode('utf-8').strip()),
                                   "id_subject": escape(request.form.get('subject').encode('utf-8').strip()),
                                   "type_work": workType, "spaced": escape(request.form.get('spaced')),
                                   "id_assignment": escape(request.form.get('paperType'))},
                                  " Where (uid='{0}') and (id_site = '{1}') ".format(
                                      escape(request.form.get('idorder').encode('utf-8').strip()), str(site_id)))
                lastid = Orders().get_id_by_uid(escape(request.form.get('idorder').encode('utf-8').strip()), session['site_id'])[0].get(
                    'id')
                files = request.files.getlist('inputfl[]')
                # ##logging.info(files)
                for file in files:
                    hash = hashlib.sha1()
                    hash.update(str(time.time()))
                    if file:
                        realname = escape(file.filename)
                        filename = hash.hexdigest()[:12] + secure_filename(file.filename)
                        logging.info(
                            "Insert INFO name:{0} path:{1} id_order:{2} id_customer:{3} date:{4}".format(realname,
                                                                                                         filename,
                                                                                                         lastid, str(
                                    session['id']), curdatetime))
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        Files().addfile(
                            {"name": realname, "path": filename, "id_order": lastid, "id_customer": str(session['id']),
                             "date": curdatetime})
                        # Orders().updorder({"pages":int(request.form.get('pages'))}," Where (uid='{0}')".format(request.form.get('idorder')))
            return jsonify(result="good")

        # ##logging.info("json = {0}".format(request.json))
        if (request.json):

            if request.json.get('price_on_date') is not None:
                # ##for rc in request.json:
                # ##logging.info("{0} = {1}".format(rc,request.json.get(rc)))
                price_on_date = escape(request.json.get('price_on_date'))
                list_price = Prices().Get_Price_For_Work_JSON(price_on_date)
                # ##logging.info("list_price= {0}".format(list_price))
                list_price_space_kof = Prices().Get_Kof_Count_Space_JSON(price_on_date)
                # ##logging.info("list_price_space_kof= {0}".format(list_price_space_kof))
                return jsonify(result=list_price, result2=list_price_space_kof)

            if request.json.get('remfile') is not None:
                # ##logging.info("json = {0}".format(request.json))
                quest_inf = {}
                quest_inf['delflag'] = 1
                # ##logging.info(" Where (path='{0}') and (id_customer = '{1}')".format(request.json.get('path'),str(session['id'])))
                Files().updfile(quest_inf,
                                " Where (path='{0}') and (id_customer = '{1}')".format(escape(request.json.get('path')),
                                                                                       str(session['id'])))
                return jsonify(result="good")

            if request.json.get('ppe') is not None:
                logging.info("json = {0}".format(request.json))
                long_msg_err = PayPalErr().Get_Sys_LongMsg(escape(request.json.get('ppe')))
                if long_msg_err:
                    if len(long_msg_err) > 0:
                        return jsonify(result=long_msg_err)
                logging.info('[e] PayPal ERROR = {0}'.format(request.json.get('ppe')))
                return jsonify(result="")

            if request.json.get('getpriceorder') is not None:
                uid = escape(request.json.get('id'))
                id_order = Orders().get_id_by_uid(uid, session['site_id'])[0].get('id')
                userorders = list(Orders().get_all_ordersid_byuser(session['id'], session['site_id']))
                xx = [int(x['id']) for x in userorders]
                prc = "0.0"
                variant = "1"
                category = ""
                name_topic = ""
                brand = ""
                coupon = ""
                status_order = ""

                if int(id_order) in xx:
                    orderslist = Orders().get_full_order(id_order)
                    if (orderslist):
                        for orders in orderslist:
                            # ##logging.info("id_order_status = {0}".format(orders["id_order_status"]))

                            prc = str(orders["price"])
                            variant = str(orders["type_work"])
                            category = str(orders["assignment"])
                            name_topic = str(orders["topic"])
                            brand = str(orders["paper_format"])
                            coupon = str(orders["discount_code"])
                            status_order = str(orders["id_order_status"])
                else:
                    abort(404)
                # ##logging.info("json = {0}".format(request.json))
                # ##print "json = {0}".format(request.json)
                return jsonify(result=str(prc),
                               variant=str(variant),
                               category=str(category),
                               name_topic=str(name_topic),
                               brand=str(brand),
                               coupon=str(coupon),
                               status_order=str(status_order))

            if (request.json.get('rem_ord') is not None):
                uid = escape(request.json.get('id'))
                id_order = Orders().get_id_by_uid(uid, session['site_id'])[0].get('id')
                userorders = list(Orders().get_all_ordersid_byuser(session['id'], session['site_id']))
                xx = [int(x['id']) for x in userorders]

                if int(id_order) in xx:
                    del_id_customer = SysConst(APP_ROOT).Get_Sys_Const("del_id_customer")
                    # ##logging.info("del_id_customer = {0}".format(del_id_customer))
                    # ##logging.info("uid = {0}".format(uid))
                    Orders().updorder({"id_customer": del_id_customer},
                                      " Where (uid='{0}') and (id_site = '{1}') ".format(uid, str(site_id)))

                else:
                    abort(404)
                # ##logging.info("json = {0}".format(request.json))
                return jsonify(result="good")

    return jsonify(result="bad")



html_escape_table = {"&": "&amp;", '"': "&quot;", "'": "&apos;", ">": "&gt;", "<": "&lt;", "«": "&laquo;",
                     "»": "&raquo;", "′": "&prime;", "″": "&Prime;", "‘": "&lsquo;", "’": "&rsquo;", "“": "&ldquo;",
                     "”": "&rdquo;", "„": "&bdquo;", "‹": "&lsaquo;", "›": "&rsaquo;", "“": "&#34;", "`": "&#96;"}

html_escape_table_delete = {"&": "", '"': "", "'": "", ">": "", "<": "", "«": "", "»": "", "′": "", "″": "", "‘": "",
                            "’": "", "“": "", "”": "", "„": "", "‹": "", "›": "", "“": "", "`": ""}


def html_escape(text, del_escape=0):
    if (del_escape == 0):
        return "".join(html_escape_table.get(c, c) for c in text)
    else:
        return "".join(html_escape_table_delete.get(c, c) for c in text)


# Mail Send
def send_mail_to_support(lastid, price):
    # mail_list = [str(SysConst(APP_ROOT).Get_Sys_Const("byvladislav")), str(SysConst(APP_ROOT).Get_Sys_Const("stanly.solano")), str(SysConst(APP_ROOT).Get_Sys_Const("zanoga.maxim")), str(SysConst(APP_ROOT).Get_Sys_Const("dimitriy.shevchenko"))]
    mail_list = (str(SysConst(APP_ROOT).Get_Sys_Const("support_mail"))).split(',')
    for mail_to in mail_list:
        print mail_to
        send_mail_from_server('New Order ' + str(lastid), mail_to, '', '<strong>New Order:</strong> ' + str(
            lastid) + ' <br><strong>Site:</strong> ' + site_name + ' <br><strong>Price:</strong> ' + str(price))
# End Mail Send


def allowed_file(filename):
    new_filename = filename.lower()
    return '.' in new_filename and \
           new_filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_filetype(ftype):
    if any(ext in ftype for ext in ALLOWED_FILETYPE):
        return True
    else:
        return False


def escape(str):
    if str is None: return None
    return escape_string(str)


def GetDateTimeToUTC(dt, time_zone="America/New_York"):
    local = pytz.timezone(time_zone)
    local_dt = local.localize(dt, is_dst=None)
    d = local_dt.astimezone(pytz.utc)
    return d


def GetUrgency(d2):
    urgency = 0
    try:
        d1 = GetDateTimeToUTC(datetime.datetime.strptime(str(datetime.datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d"))
        # ##logging.info("d1= {0}".format(d1))
        d2 = GetDateTimeToUTC(datetime.datetime.strptime(str(d2), "%Y-%m-%d"))
        # ##logging.info("d2= {0}".format(d2))
        urgency = (d2 - d1).days
        # ##logging.info("END urgency (0) ={0}".format(str(urgency)))
        if (urgency < -1):
            urgency = -1
        # ##logging.info("END urgency (1) ={0}".format(str(urgency)))
        if (((d2 - d1).seconds // 3600) > 0):
            urgency += 1
        # ##logging.info("END urgency (2) ={0}".format(str(urgency)))
        # ##logging.info("(d2-d1).days={0}".format(str((d2-d1).days)))
        # ##logging.info("(d2-d1).seconds // 3600={0}".format(str((d2-d1).seconds // 3600)))
        if (urgency > 30):
            urgency = 30
        if (urgency < 0):
            urgency = 0
    except Exception, e:
        logging.info('[e] GetUrgency ERROR = {0}; Input data D2 = {1}'.format(e, str(d2)))
    return urgency


def GetCurentPriceForWork(wt, al, dd, spc, p, d):
    """
        wt  -   Type of work     (1 - Writing from scratch / 2 - Editing / 3 - Slides)
        al  -   Academic level   (1-High school, 2-College, 3-University, 4-Masters, 5-Ph.D.)
        dd  -   Deadline (in day 0, 1, 2, 3, 5, 7, 9, 30)
        spc -   Spacing (1 or 2)
        p   -   Count pages
        d   -   Discount
    """
    spc_ = spc if (not spc is None) else 1
    wt_ = wt if (not wt is None) else 1
    al_ = al if (not al is None) else 1
    dd_ = dd if (not dd is None) else 1
    p_ = p if (not p is None) else 1
    d_ = d if (not d is None) else " "
    # print "d ={0}".format(str(d))
    # print "d_ ={0}".format(str(d_))
    price_with_discount = None
    kof_space = Prices(APP_ROOT).Get_Kof_Count_Space(spc_)
    if str(wt_) == '3':
        kof_space = 1
    price_without_discount = Prices(APP_ROOT).Get_Price_For_Work(
        wt_,
        al_,
        dd_,
        kof_space,
        p_
    )
    # ##logging.info("price_without_discount={0}".format(str(price_without_discount)))
    if d_ == " ":
        return price_without_discount

    if price_without_discount is not None:
        price_with_discount = round((1.0 - float(Orders().get_discount(d_)) / 100) * float(price_without_discount), 2)
    return price_with_discount


def ShortSiteName(sn):
    return str(sn).replace('https', '').replace('http', '').replace(':', '').replace('/', '')


def GetIdExtraOrder(uid):
    id = None
    try:
        if "_" in uid:
            id = uid.split("_")[1]
            if len(id) <= 0:
                id = None
    except Exception, e:
        logging.info("[e] ERROR in GetIdExtraOrder : {}".format(e))
        id = None
    return id


def SendRequestToSystem(id_req, **kwargs):
    if id_req == 1:
        headers = {"X-Auth-Token": kwargs.get("header1")}
        url = kwargs.get("url1", URL_SYSTEM)
        data = {"id_extra_order": kwargs.get("data1"), "id_order": kwargs.get("data2")}
        req = requests.post(url, data=data, headers=headers)
        Events().add_event(str(kwargs.get("data1")) + " extraorder send request to system " + str(
            session['id']) + ", response from SYSTEM {}".format(str(req.status_code)),
                           82, kwargs.get("data2"), session['id'])


# Work with file end

# --- START FILTERS ---
# ----------------------------------------------------------------------------

@app.template_filter('GetPriceWork')
def GetPriceWork(wrk):
    # Get price for work from DB
    try:
        price_without_discount = Prices(APP_ROOT).Get_Price_For_Work(
            wrk[0],
            wrk[1],
            wrk[2],
            wrk[3],
            wrk[4]
        );
        #        print wrk
        #        print price_without_discount
        #        print "-----------"
        # logging.info("[e] price_without_discount : {}".format(price_without_discount))
        # logging.info("[e] new price_without_discount : {}".format("{:.2f}".format(float(price_without_discount))))
        return "{0:.2f}".format(float(price_without_discount))
    except Exception, e:
        raise
    return "n/a"


@app.template_filter('TargetWork')
def TargetWork(wrk):
    # Get price for work from DB
    try:
        if (wrk == 1):
            return "High School"
        elif (wrk == 2):
            return "College"
        elif (wrk == 3):
            return "University"
        elif (wrk == 4):
            return "Master’s"
        elif (wrk == 5):
            return "Ph.D."
    except Exception, e:
        raise
    return "n/a"


@app.template_filter('ShortDateFormat')
def ShortDateFormat(dt):
    #    create a dictionary for the months
    date_format_short = '%Y-%m-%d'
    date_format_long = '%Y-%m-%d %H:%M:%S'
    # formated date
    try:
        dt_ = str(dt)
        rc = datetime.datetime.strptime(dt_, date_format_long)
        return rc.strftime(date_format_short)
    except Exception, e:
        raise
    return "-"


@app.template_filter('ShowDateFormat')
def ShowDateFormat(dt):
    #    create a dictionary for the months
    date_format_long = '%Y-%m-%d %H:%M:%S'
    date_format = '%b %d, %Y at %H:%M'
    # formated date
    try:
        dt_ = str(dt)
        rc = datetime.datetime.strptime(dt_, date_format_long)
        return rc.strftime(date_format)
    except Exception, e:
        logging.info("[e] ERROR in ShowDateFormat : {}".format(e))
        pass
    return "-"


@app.template_filter('len_obj')
def len_obj(l_o):
    try:
        return len(l_o)
    except Exception:
        return 0
    else:
        pass
    finally:
        pass


@app.template_filter('uni_ascci')
def unicodetoascii(text):
    text = text.replace('\xe2\x80\x99', "'")
    text = text.replace('\xe2\x80\x9c', '"')
    text = text.replace('\xe2\x80\x9d', '"')
    text = text.replace('\xe2\x80\x9e', '"')
    text = text.replace('\xe2\x80\x9f', '"')
    text = text.replace('\xc3\xa9', 'e')
    text = text.replace('\xe2\x80\x9c', '"')
    text = text.replace('\xe2\x80\x93', '-')
    text = text.replace('\xe2\x80\x92', '-')
    text = text.replace('\xe2\x80\x94', '-')
    text = text.replace('\xe2\x80\x94', '-')
    text = text.replace('\xe2\x80\x98', "'")
    text = text.replace('\xe2\x80\x9b', "'")
    text = text.replace('\xe2\x80\x90', '-')
    text = text.replace('\xe2\x80\x91', '-')
    text = text.replace('\xe2\x80\xb2', "'")
    text = text.replace('\xe2\x80\xb3', "'")
    text = text.replace('\xe2\x80\xb4', "'")
    text = text.replace('\xe2\x80\xb5', "'")
    text = text.replace('\xe2\x80\xb6', "'")
    text = text.replace('\xe2\x80\xb7', "'")
    text = text.replace('\xe2\x81\xba', "+")
    text = text.replace('\xe2\x81\xbb', "-")
    text = text.replace('\xe2\x81\xbc', "=")
    text = text.replace('\xe2\x81\xbd', "(")
    text = text.replace('\xe2\x81\xbe', ")")
    encodings = ['utf8', 'latin1', 'cp1252', 'cp1251']
    rez = ""
    for enc in encodings:
        try:
            rez = text.decode(enc).encode('utf8')
            # ##logging.info("encode rez={0}".format(str(text.encode('utf8'))))
            # ##logging.info("unicodetoascii rez={0}".format(str(rez)))
            break
        except Exception, e:
            continue
        else:
            pass
        finally:
            pass
    return rez


# --- END FILTERS ---

# --- START STATUC ---
# ----------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
@app.route('/index.html')
def GlobalParseUrlForContentIndex():
    # UserCheck("test", "test")
    # Work_UserCheck().get_all()
    try:
        page_url = "'/index','/index.html','/'"
        ###logging.info("GlobalParseUrlForContentIndex page_url = {0}".format(str(page_url)))
        list_contents = SysConst(APP_ROOT).GetHTML_Content_Pages(page_url)
        ###logging.info("list_contents={0}".format(list_contents))
        list_contents_include = SysConst(APP_ROOT).GetHTML_Include_Content_Pages()
        ###logging.info("list_contents_include={0}".format(list_contents_include))
        ###logging.info("block_body_={0}".format(block_body_))
        template_pages = SysConst(APP_ROOT).Get_Template_Pages(page_url)
        ###logging.info("template_pages= {0}".format(template_pages))
        if (template_pages is None):
            abort(404)
        if (len(template_pages) < 1):
            abort(404)
    except Exception, e:
        logging.info("ERROR = {0}".format(e))
        abort(404)
    return render_template(template_pages,
                           list_contents=list_contents,
                           site_name = site_name,
                           list_contents_include=list_contents_include
                           )


def update_data(id):
    site_data = Api(Wrapper()).get_data_by_id(id)
    global site_name
    site_name = site_data[0]['site_name']
    global site_mail
    site_mail = site_data[0]['site_mail']
    global site_pass
    site_pass = site_data[0]['site_pass']
    global site_noreply_mail
    site_noreply_mail = site_data[0]['noreply_mail']
    global site_noreply_pass
    site_noreply_pass = site_data[0]['noreply_pass']




@app.route('/test')
def test():
    return jsonify(site_name)




@app.route('/api/site_identity', methods=['POST'])
@cross_origin(supports_credentials=True)
def api_site_indentity():
    if request.method == 'POST':
        result = {}
        f = request.form
        result = {}
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        site = request.json.get('site')
        s = Sites(Wrapper()).check_site(site)
        if session.get('site_id'):
        	if s[0]['id'] == session['site_id']:
        		return jsonify(s[0]['id'])
	        else:
	        	return jsonify(s[0]['id'])
    	else:
    		return jsonify(s[0]['id'])

        # if s:
        #     return jsonify(s[0]['id'])
        # return jsonify(s)


@app.route('/api/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def api_login():
    if request.method == 'POST':
        result = {}
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        if Users().api_login({"email": result.get("email"), "password": result.get("password")}, result.get("site_id")):
            id_user = Users().get_customer_id(escape(result.get("email")), escape(result.get("site_id")))
            data = {}
            data['id'] = id_user[0].get('id')
            data['logged_in'] = True
            data['site_id'] = result.get("site_id")
            session['id'] = id_user[0].get('id')
            session['site_id'] = result.get("site_id")
            session['logged_in'] = True
            update_data(session['site_id'])
            return json.dumps(data)
        else:
            return "1"



@app.route("/api/loginform")
@cross_origin(supports_credentials=True)
def login_form():
    return render_template('customer-login.html')




@app.route('/api/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def api_register():
    if request.method == 'POST':
        result = {}
        f = request.form
        result = {}
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                result[key] = value
        site = request.json.get('site')
        s = Sites(Wrapper()).check_site(site)
        if s:
            return jsonify(s[0]['id'])
        return jsonify(s)


if __name__ == "__main__":
    app.run(debug=True)
else:
    logging.basicConfig(debug=True, threaded=True,host='0.0.0.0', port=5000)
