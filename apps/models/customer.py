from wrapper import Wrapper
from conf import Conf
from apps.utils.utils import send_mail
from apps.utils.utils import send_mail_from_server
from sys_const import SysConst
from extraorders import Extraorders
from templateletter import TemlateLetter
import re
import random


class Customer(object):
    table_name = "Customers"
    table_orders = "Orders"
    site_name = str(SysConst().Get_Sys_Const("site_name"))
    site_name_short = str(site_name).replace('https', '').replace('http', '').replace(':', '').replace('/', '')
    site_mail = str(SysConst().Get_Sys_Const("site_mail"))
    site_pass = str(SysConst().Get_Sys_Const("site_pass"))
    tsm_mail_address = str(SysConst().Get_Sys_Const("tsm_mail_address"))
    tsm_mail_pass = str(SysConst().Get_Sys_Const("tsm_mail_pass"))
    site_id = str(SysConst().Get_Sys_Const("site_id"))

    site_noreply_mail = str(SysConst().Get_Sys_Const("noreply_mail"))
    site_noreply_pass = str(SysConst().Get_Sys_Const("noreply_pass"))

    def __init__(self):
        self.w = Wrapper()

    def send_mail_to_support_from_contactform(self, name, mail, message, phone=""):
        ###print "site_noreply_mail : {0}".format(self.site_noreply_mail)
        ###print "site_noreply_pass : {0}".format(self.site_noreply_pass)
        msg = "Name: {1}<br>Email: {0}<br>Phone: {3}<br>Message: {2}".format(mail, str(name).lower().title(), message,
                                                                             phone)
        msg_send = TemlateLetter().get_template_letter("", "", msg, self.site_name_short, self.site_mail,
                                                       self.site_name)
        send_mail(self.site_noreply_mail,
                  self.site_noreply_pass,
                  self.site_noreply_mail,
                  self.site_mail,
                  "Contact form message {0}".format(self.site_name_short),
                  "",
                  msg_send)

    def get_customer_info_by_order(self, orderid,site_id):
        return self.w.select("email,first_name,last_name,phone", self.table_name,
                             " where id=(select id_customer from {1} where id={0}) ".format(orderid, self.table_orders) +
                             " and (id_site = '{0}') ".format(site_id))

    def send_mail_to_client(self, orderid):
        customer_info = self.get_customer_info_by_order(orderid)[0]
        uid = self.w.select("uid", self.table_orders, " where id={0}".format(orderid))[0].get('uid')
        # msg = "Hello, dear <i>{1} {2}</i>, <br><br> Your order <i>{0}</i> was successfully created.<br><br> We are ready to start working on it as soon as the payment is made.<br> Please, proceed to <a href=http://pro-essay-writer.com/dashboard>http://pro-essay-writer.com/dashboard</a> to complete your payment!<br><br> ---<br>Pro-Essay-Writer support team!<br>1(888) 308-3358<br><a href=mailto:support@pro-essay-writer.com>support@pro-essay-writer.com</a><br><a href=http://pro-essay-writer.com>pro-essay-writer.com</a><br>".format(uid,customer_info.get('first_name'),customer_info.get('last_name'))
        first_name = customer_info.get('first_name')
        if (str(first_name).strip() == '-'):
            first_name = "Client"
        last_name = customer_info.get('last_name')
        if (str(last_name).strip() == '-'):
            last_name = ""

        msg = "Hello, dear <i>{0}</i>,<br>".format(first_name.lower().title()) + (
            str(SysConst().Get_Sys_Const("send_mail_to_client"))).format(uid)
        msg_send = TemlateLetter().get_template_letter("", "", msg, " ", self.site_mail, self.site_name)
        send_mail(self.site_mail, self.site_pass, "{0} <{1}>".format(self.site_name_short, self.site_mail),
                  customer_info.get('email'), "Order {0} created".format(uid), "", msg_send)
        # send_mail_from_server("Your order was successfully created.", customer_info.get('email'), "", msg)

    def send_mail_to_client_payment(self, orderid):
        customer_info = self.get_customer_info_by_order(orderid)[0]
        uid = self.w.select("uid", self.table_orders, " where id={0}".format(orderid))[0].get('uid')
        # msg = "Greetings, dear {1} {2}, <br> Your order <strong>{0}</strong> is now being processed.<br> We are going to start working on it right away!<br> Thank you for choosing pro-essay-writer.com. <br><br> ---<br>Pro-Essay-Writer support team!<br>1(888) 308-3358<br><a href=mailto:support@pro-essay-writer.com>support@pro-essay-writer.com</a><br><a href=http://pro-essay-writer.com>pro-essay-writer.com</a><br>".format(uid,customer_info.get('first_name'),customer_info.get('last_name'))
        first_name = customer_info.get('first_name')
        if (str(first_name).strip() == '-'):
            first_name = "Client"
        msg = "Hello, dear <i>{0}</i>,<br>".format(str(first_name).lower().title()) + (
            str(SysConst().Get_Sys_Const("send_mail_to_client_payment"))).format(uid)
        msg_send = TemlateLetter().get_template_letter("", "", msg, " ", self.site_mail, self.site_name)
        send_mail(self.site_mail, self.site_pass, "{0} <{1}>".format(self.site_name_short, self.site_mail),
                  customer_info.get('email'), "Order {0} has been paid".format(uid), "", msg_send)

    def send_mail_to_support_payment(self, orderid, extrordid=None):
        # tsm_mail_list = [str(SysConst().Get_Sys_Const("byvladislav")), str(SysConst().Get_Sys_Const("stanly.solano")), str(SysConst().Get_Sys_Const("zanoga.maxim")), str(SysConst().Get_Sys_Const("dimitriy.shevchenko"))]
        tsm_mail_list = (str(SysConst().Get_Sys_Const("support_mail"))).split(',')
        customer_info = self.get_customer_info_by_order(orderid)[0]
        order_info = self.w.select("*", self.table_orders, "where id={0}".format(orderid))[0]
        for x in tsm_mail_list:
            ###send_mail(self.tsm_mail_address, self.tsm_mail_pass, self.tsm_mail_address, x,"Order has been PAID! [ {0} ]".format(self.site_name), "","Order ID: {0}<br>UID: {4}<br>Client mail: {1}<br>First name: {2}<br>Last name: {3}<br><br>Price: <strong>${5}</strong><br>DeadLine: <strong>{6}</strong>".format(orderid,customer_info.get('email'),customer_info.get('first_name'),customer_info.get('last_name'),order_info.get('uid'),order_info.get('price'),order_info.get('deadline')))
            if extrordid:
                wrap = Wrapper()
                extra_price = Extraorders(wrap).get_surcharge_paid(extrordid)
                msg = "Hello Support!<br>Order ID: {0}, Extra Order ID: {7}<br>UID: {4}<br>Client mail: {1}<br>First name: {2}<br>Last name: {3}<br><br>Extra price: <strong>${5}</strong><br>DeadLine: <strong>{6}</strong>".format(
                    orderid, customer_info.get('email'), str(customer_info.get('first_name')).lower().title(),
                    str(customer_info.get('last_name')).lower().title(), order_info.get('uid'),
                    extra_price[0].get('final_order_surcharge'),
                    order_info.get('deadline'), str(extrordid))
            else:
                msg = "Hello Support!<br>Order ID: {0}<br>UID: {4}<br>Client mail: {1}<br>First name: {2}<br>Last name: {3}<br><br>Price: <strong>${5}</strong><br>DeadLine: <strong>{6}</strong>".format(
                    orderid, customer_info.get('email'), str(customer_info.get('first_name')).lower().title(),
                    str(customer_info.get('last_name')).lower().title(), order_info.get('uid'), order_info.get('price'),
                    order_info.get('deadline'))
            msg_send = TemlateLetter().get_template_letter("", "", msg, "Customer", self.site_mail, self.site_name)
            send_mail(self.tsm_mail_address, self.tsm_mail_pass, self.tsm_mail_address, x,
                      "Order has been PAID! [ {0} ]".format(self.site_name), "", msg_send)

    def checkmail(self, mail):
        return self.w.select("id", self.table_name, " where email='{0}' ".format(mail) +
                             " and (id_site = '{0}') ".format(self.site_id))

    def get_customer_info(self, userid, site_id):
        return self.w.select("*", self.table_name, " where id={0} ".format(userid) +
                             " and (id_site = '{0}') ".format(site_id))

    def customer_profile_update(self, userid, fname, phone, country='', email='', newsletters=1):
        upd_prof = -1
        try:
            upd_prof = self.w.update(
                {"first_name": fname, "phone": phone, "country": country, "email": email, "newsletters": newsletters},
                self.table_name, " where id={0} ".format(userid) +
                                 " and (id_site = '{0}') ".format(self.site_id))
        except Exception, e:
            print "Exception : {0}".format(e)
        finally:
            first_name = fname
            if (str(fname).strip() == '-'):
                first_name = "Client"
            msg = "Hello, dear <i>{0}</i>,<br>".format(first_name.lower().title()) + \
                  "You have updated your profile information. Kindly refer to the data below:<br>" + \
                  "Email: <i>{0}</i><br>".format(email) + \
                  "Name: <i>{0}</i><br>".format(first_name) + \
                  "Phone: <i>{0}</i><br>".format(phone) + \
                  "Warm regards<br><hr>" + \
                  "{0} support team<br>".format(self.site_name_short) + \
                  "{0}".format(self.site_mail)
            msg_send = TemlateLetter().get_template_letter("", "", msg, " ", self.site_mail, self.site_name)
            send_mail(self.site_mail, self.site_pass, "{0} <{1}>".format(self.site_name_short, self.site_mail), email,
                      "Your profile has been updated", "", msg_send)
        return upd_prof

    def customer_password_update(self, userid, oldpassword, newpassword):
        old = self.w.select("password", self.table_name, " where id={0} ".format(userid)+
                            " and (id_site = '{0}') ".format(self.site_id))[0]
        fname = self.w.select("first_name", self.table_name, " where id={0} ".format(userid) +
                              " and (id_site = '{0}') ".format(self.site_id))[0].get("first_name")
        email = self.w.select("email", self.table_name, " where id={0} ".format(userid) +
                              " and (id_site = '{0}') ".format(self.site_id))[0].get("email")
        ###print email
        ###print fname
        if (oldpassword == old.get("password")):
            self.w.update({"password": newpassword}, self.table_name, " where id={0} ".format(userid) +
                          " and (id_site = '{0}') ".format(self.site_id))
            first_name = fname
            if (str(first_name).strip() == '-'):
                first_name = "Client"
            msg = "Hello, dear <i>{0}</i>,<br>".format(first_name.lower().title()) + \
                  "You have updated your password.<br>" + \
                  "New password: <i>{0}</i><br>".format(newpassword) + \
                  "Warm regards<br><hr>" + \
                  "{0} support team<br>".format(self.site_name_short) + \
                  "{0}".format(self.site_mail)
            msg_send = TemlateLetter().get_template_letter("", "", msg, " ", self.site_mail, self.site_name)
            send_mail(self.site_noreply_mail, self.site_noreply_pass,
                      "{0} <{1}>".format(self.site_name_short, self.site_noreply_mail), email,
                      "Your profile has been updated", "", msg_send)
            return "ok"
        else:
            return "error"

    def __generate_password(self):
        chars = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz', 62)
        return ''.join(random.choice(chars) for _ in xrange(0, random.randint(7, 10)))

    def is_email_exists(self, email):
        return True if self.w.select(['id', 'email'], self.table_name, ' where email="{0}" '.format(email) +
                                     " and (id_site = '{0}') ".format(self.site_id)) else False

    def reset_password(self, email):
        data = self.w.select(['id', 'email', 'first_name', 'last_name'], self.table_name,
                             ' where email="{0}" '.format(email) +
                             " and (id_site = '{0}') ".format(self.site_id))
        if data:
            new_password = self.__generate_password()
            self.w.update({'password': new_password}, self.table_name, 'where id=%s' % data[0]['id'])
            first_name = data[0]['first_name']
            if (str(first_name).strip() == '-'):
                first_name = "Client"
            message = "Hello, dear <i>{0}</i>,<br>".format(str(first_name).lower().title()) + \
                      "Your password has been reset. <br>" + \
                      "New password: <i>{0}</i><br>".format(new_password) + \
                      "Warm regards<br><hr>" + \
                      "{0} support team<br>".format(self.site_name_short) + \
                      "{0}".format(self.site_mail)
            ###message = 'You have requested password recovery. Your new password is %s ' % new_password
            ###send_mail(self.site_mail, self.site_pass, self.site_mail, email, "Reset your password", message, "")

            msg_send = TemlateLetter().get_template_letter("", "", message, "", self.site_mail, self.site_name)
            send_mail(self.site_mail, self.site_pass, "{0} <{1}>".format(self.site_name_short, self.site_mail), email,
                      "Password reset for {0}".format(self.site_name_short), "", msg_send)
            return True
        else:
            return False
