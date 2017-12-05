import time
import datetime
import logging

from wrapper import Wrapper
from apps.models.orders import Orders


class Extraorders(object):
    table_name = "ExtraOrders"
    table_order = "Orders"
    TIME_HOUR_WAIT_TO_PAY_EXTRAORDER = "6"
    # self.ID_ORDER_STATUS = 1 - not payed
    ID_ORDER_STATUS = 1

    def __init__(self, wrapper):
        if wrapper is None:
            raise TypeError

        self.w = wrapper

    def add_trans_id(self, fields, id_extraord=""):
        """
        Add id transaction into EXTAORDERS
        :param fields: list update fields
        :param id_extraord: condition
        :return:
        """
        return self.w.update(fields, self.table_name, " where id='{}' ".format(id_extraord))

    def get_surcharge(self, id_ord):
        """
        Get from surcharge EXTAORDERS
        :param id_extraord: id extraorders
        :return: surcharge
        """
        return self.w.select(" final_order_price ", self.table_name,
                             " where id_order='{0}' and id_order_status={1} ".format(id_ord, self.ID_ORDER_STATUS))

    def get_surcharge_paid(self, id_extr_ord):
        """
        Get from surcharge EXTAORDERS
        :param id_extraord: id extraorders
        :return: surcharge paid
        """
        return self.w.select(" final_order_surcharge ", self.table_name,
                             " where id='{0}' ".format(id_extr_ord))

    def can_pay_extraoder(self, id_ord):
        """
        Check is can customer pay extraorder
        :param id_ord: id orders
        :return: true - can pay / false - can't pay
        """
        can_pay_extra_order = None
        try:
            can_pay_extra_order = \
                self.w.select(" IF(HOUR(TIMEDIFF(NOW(),e.date_created))>={0},1,0) as can_pay_extra_order ".format(
                    self.TIME_HOUR_WAIT_TO_PAY_EXTRAORDER), self.table_name,
                    " as e where id_order='{0}' and id_order_status={1} ".format(id_ord, self.ID_ORDER_STATUS))[0].get(
                    'can_pay_extra_order')
        except Exception, e:
            logging.info(" [E] ERROR in can_pay_extraoder : {}  ".format(e))
        finally:
            pass
        return can_pay_extra_order == 0

    def assign_extraorder(self, id_extra_orsder):
        """
        Copy field from EXTRAORDER to ORDER
        :param id_extra_orsder: id extraorder
        :return: true if sucsses insert into table order
        """
        try:
            extr_ord_field = self.w.select(
                " extr_ord.pages, extr_ord.urgency, extr_ord.id_academic_level, extr_ord.id_order, " +
                " extr_ord.final_order_surcharge, extr_ord.basic_order_surcharge, " +
                " extr_ord.discount_code, extr_ord.discount_percent, " +
                " extr_ord.final_order_price, extr_ord.basic_order_price, ord.id_writer ",
                self.table_name,
                (" as extr_ord " +
                 " left join " +
                 " {1} as ord " +
                 " on " +
                 " extr_ord.id_order=ord.id "
                 " where extr_ord.id='{0}' " +
                 " ").format(id_extra_orsder, self.table_order)
                )
            if extr_ord_field:
                bsc_price_order = extr_ord_field[0].get('basic_order_surcharge')
                fnl_price_order = extr_ord_field[0].get('fianl_order_surcharge')
                final_order_price = extr_ord_field[0].get('final_order_price')
                basic_order_price = extr_ord_field[0].get('basic_order_price')
                pages = extr_ord_field[0].get('pages')
                id_ac_lvl = extr_ord_field[0].get('id_academic_level')
                id_ord = extr_ord_field[0].get('id_order')
                urgency = extr_ord_field[0].get('urgency')
                discount_code = extr_ord_field[0].get('discount_code')
                discount_percent = extr_ord_field[0].get('discount_percent')
                id_writer = extr_ord_field[0].get('id_writer')
                # payd order status = 2
                id_order_status = 2
                if id_writer:
                    # in progress order status = 3
                    id_order_status = 3

                # if urgency < 0 that mean deadline (writers and customers) don't change
                if float(urgency) < 0:
                    Orders().updorder({"price": final_order_price,
                                       "discount": discount_percent,
                                       "pages": pages,
                                       "id_academic_level": id_ac_lvl,
                                       "discount_code": discount_code,
                                       "basic_price": basic_order_price,
                                       "id_order_status": id_order_status},
                                      " Where (id='{0}') ".format(id_ord)
                                      )
                else:
                    CurentDate = time.strftime("%Y-%m-%d %H:%M:%S")
                    Date = datetime.datetime.strptime(CurentDate, "%Y-%m-%d %H:%M:%S")
                    client_dl = Date
                    writer_dl = Date
                    if urgency == '0.12' or urgency == '0':
                        client_dl = Date + datetime.timedelta(hours=12)
                        writer_dl = Date + datetime.timedelta(hours=9)
                    else:
                        client_dl = Date + datetime.timedelta(days=int(urgency))
                        writer_dl = Date + datetime.timedelta(days=(int(urgency) * 0.75))

                    Orders().updorder({"price": final_order_price,
                                       "urgency": urgency,
                                       "discount": discount_percent,
                                       "deadline": client_dl,
                                       "wr_deadline": writer_dl,
                                       "pages": pages,
                                       "id_academic_level": id_ac_lvl,
                                       "discount_code": discount_code,
                                       "basic_price": basic_order_price,
                                       "id_order_status": id_order_status},
                                      " Where (id='{0}') ".format(id_ord)
                                      )

        except Exception, e:
            logging.info(" [E] ERROR in assign_extraorder : {}  ".format(e))
        finally:
            pass
