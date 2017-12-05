import time
import datetime

from wrapper import Wrapper
from apps.models.orders import Orders


class Extraorders(object):
    table_name = "ExtraOrders"
    table_order = "Orders"

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
        ID_ORDER_STATUS = 1
        return self.w.select(" fnl_price_order ", self.table_name,
                             " where id_order='{0}' and id_order_status={1} ".format(id_ord, ID_ORDER_STATUS))

    def assign_extraorder(self, id_extra_orsder):
        """
        Copy field from EXTRAORDER to ORDER
        :param id_extra_orsder: id extraorder
        :return: true if sucsses insert into table order
        """
        try:
            extr_ord_field = self.w.select(" pages, urgency, id_academic_level, id_order, " +
                                           " final_order_surcharge, basic_order_surcharge, " +
                                           " final_order_price ",
                                           self.table_name,
                                           (" as extr_ord " +
                                            " where extr_ord.id={0} " +
                                            " ").format(id_extra_orsder)
                                           )
            if extr_ord_field:
                bsc_price_order = extr_ord_field[0].get('basic_order_surcharge')
                fnl_price_order = extr_ord_field[0].get('fianl_order_surcharge')
                pages = extr_ord_field[0].get('pages')
                id_ac_lvl = extr_ord_field[0].get('id_academic_level')
                id_ord = extr_ord_field[0].get('id_order')
                urgency = extr_ord_field[0].get('urgency')
                # in progress order status = 3
                id_order_status = 3

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

                Orders().updorder({"price": fnl_price_order, "urgency": urgency, "discount": 0,
                                   "deadline": client_dl,
                                   "wr_deadline": writer_dl,
                                   "pages": pages,
                                   "id_academic_level": id_ac_lvl,
                                   "discount_code": "-",
                                   "id_order_status": id_order_status},
                                  " Where (uid='{0}') ".format(id_ord)
                                  )

        except Exception, e:
            print e
        finally:
            pass
