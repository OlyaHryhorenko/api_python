import math
import time
import datetime
from wrapper import Wrapper
from sys_const import SysConst
from events import Events


class Orders(object):
    table_name = "Orders"
    AcademicLevels_name = "AcademicLevels"
    Assignment_name = "OrderAssignment"
    Subjects_name = "Subjects"
    OrderStatuses_name = "OrderStatuses"
    table_customer_files = "CustomerFiles"
    table_writers_files = "WriterFiles"
    discounts = "Discount"
    claimtable = "Claims"
    table_writers = "Writers"
    table_name_extra_ord = "ExtraOrders"
    site_id = str(SysConst().Get_Sys_Const("site_id"))
    SERVICES_ID_SESSION = str(SysConst().Get_Sys_Const("del_id_customer"))
    EVENT_ID_UPD_DEADLINE = 83
    TIME_HOUR_WAIT_TO_PAY_EXTRAORDER = "6"
    TIME_DAY_WAIT_AFETR_PAY_FOR_REVISION = "14"

    def __init__(self):
        self.w = Wrapper()

    def get_discount(self, discountcode):
        disc = self.w.select("percent", self.discounts, "where code='{0}'".format(discountcode))
        if (disc):
            return disc[0].get('percent')
        else:
            return str(0)

    def addorder(self, fields):
        return self.w.insert(fields, self.table_name)

    def updorder(self, fields, condition=""):
        return self.w.update(fields, self.table_name, condition)

    def get_all_ordersid_byuser(self, userid, site_id):
        return self.w.select("id", self.table_name, " where id_customer={0} ".format(userid) +
                             " and (id_site = '{0}') ".format(site_id))

    def get_odresrsbyuser(self, user_id, site_id):
        return self.w.select((" *, IF(DATEDIFF(CURDATE(), o.deadline)>{0},1,0) as revision, "
                              " IF(HOUR(TIMEDIFF(NOW(),e.date_created))>={1},1,0) as can_pay_extra_orders, "
                              " e.date_created as extr_date_create, "
                              " date_add(e.date_created, INTERVAL {1} hour) as extr_date_expired, "
                              " e.id as id_extr_ord, "
                              " e.date_paid as extr_date_paid, "
                              " e.deadline as deadline_extr_ord, "
                              " e.pages as pages_extr_ord, "
                              " e.discount_code as discount_code_extr_ord, "
                              " e.id_academic_level as id_acad_lvl_extr_ord, "
                              " e.final_order_surcharge ").format(self.TIME_DAY_WAIT_AFETR_PAY_FOR_REVISION,
                                                                  self.TIME_HOUR_WAIT_TO_PAY_EXTRAORDER),
                             self.table_name,
                             (" as o "
                              " inner join {2} as os on os.id = o.id_order_status "
                              " left join (select id_order,count(id_order) as count_file from {4} Group By id_order) as wf on wf.id_order = o.id "
                              " left join {3} as oa on o.id_assignment = oa.id "
                              " left join {0} as e on o.id=e.id_order and e.id_order_status=1 "
                              " where id_customer={1} "
                              " and (id_site = '{5}') ").format(self.table_name_extra_ord, user_id,
                                                                self.OrderStatuses_name, self.Assignment_name,
                                                                self.table_writers_files, site_id )
                             )

    def get_list_file_by_order(self, userid, site_id):
        return self.w.select("*", self.table_name,
                             (" as o left join {1} as wf on wf.id_order = o.id "
                              " Where (id_customer={0}) and (id_site = '{2}') ").format(userid,
                                                                                        self.table_writers_files,
                                                                                        site_id)
                             )

    def get_odresrsbyid(self, orderid):
        return self.w.select("*", self.table_name,
                             "where (id={0}) and (id_site = '{1}') ".format(orderid, self.site_id))

    def get_all_orders_type(self):
        return self.w.select("*", "OrderAssignment")

    def get_all_orders_subject(self):
        return self.w.select("*", "Subjects")

    def get_academic_level(self, level):
        return self.w.select("id", self.AcademicLevels_name, " where name='{0}'".format(level))

    def get_academic_level_byid(self, idlevel):
        return self.w.select("level", self.AcademicLevels_name, " where id='{0}'".format(idlevel))

    def get_assignment_level_byid(self, idlevel):
        return self.w.select("assignment", self.Assignment_name, " where id='{0}'".format(idlevel))

    def get_subjects_byid(self, idsub):
        return self.w.select("subject", self.Subjects_name, " where id='{0}'".format(idsub))

    def get_text_status(self, idstatus):
        return self.w.select("order_status", self.OrderStatuses_name, " where id='{0}'".format(idstatus))

    def get_id_by_uid(self, uid, site_id):
        return self.w.select("id", self.table_name,
                             " where (uid='{0}') and (id_site = '{1}') ".format(uid, site_id))

    def get_all_files(self, orderid):
        return self.w.select(" name,path,date,id_order ", self.table_customer_files,
                             " where id_order={0} union select name,path,date,id_order from {1} where id_order={0}".format(
                                 orderid, self.table_writers_files))

    def get_all_customer_files(self, orderid):
        return self.w.select("name, path, date, id_order, delflag", self.table_customer_files,
                             " where (id_order={0}) and (delflag <> 1)".format(orderid))

    def get_all_writers_files(self, orderid):
        return self.w.select("name, path, date, id_order", self.table_writers_files,
                             " where id_order={0}".format(orderid))

    def get_full_order(self, orderid, site_id):
        return self.w.select((" *, IF(DATEDIFF(CURDATE(), o.deadline)>{0},1,0) as revision, "
                              " IF(HOUR(TIMEDIFF(NOW(),e.date_created))>={1},1,0) as can_pay_extra_orders, "
                              " e.date_created as extr_date_create, "
                              " date_add(e.date_created, INTERVAL {1} hour) as extr_date_expired, "
                              " e.id as id_extr_ord, "
                              " e.date_paid as extr_date_paid, "
                              " e.deadline as deadline_extr_ord, "
                              " e.pages as pages_extr_ord, "
                              " e.discount_code as discount_code_extr_ord, "
                              " e.id_academic_level as id_acad_lvl_extr_ord, "
                              " e.final_order_surcharge ").format(self.TIME_DAY_WAIT_AFETR_PAY_FOR_REVISION,
                                                                  self.TIME_HOUR_WAIT_TO_PAY_EXTRAORDER),
                             self.table_name,
                             (" as o left join {3} as s on o.id_subject = s.id left "
                              " join {4} as a on o.id_academic_level = a.id left "
                              " join {2} as oa on o.id_assignment = oa.id "
                              " left join {0} as e on o.id=e.id_order and e.id_order_status=1 "
                              " where o.id = {1} "
                              " and (id_site = '{5}') ").format(self.table_name_extra_ord, orderid,
                                                                self.Assignment_name,
                                                                self.Subjects_name, self.AcademicLevels_name,
                                                                site_id)
                             )

    def get_customer_id_by_uid(self, uid):
        return self.w.select(" id_customer ", self.table_name,
                             " where uid='{0}' and (id_site = '{1}') ".format(uid, self.site_id))

    def status_change(self, orderid, status, site_id):
        cdate = time.strftime("%Y-%m-%d %H:%M:%S")
        if status == 2:
            x = self.w.update({"id_order_status": status, "payment_date": cdate},
                              self.table_name, " where uid='{0}' and (id_site = '{1}') ".format(orderid, site_id))
            self.update_dl(orderid, site_id)
            return x
        else:
            return self.w.update({"id_order_status": status}, self.table_name,
                                 " where uid='{0}' and (id_site = '{1}') ".format(orderid, site_id))

    def update_dl(self, orderid, site_id):
        CurentDate = time.strftime("%Y-%m-%d %H:%M:%S")
        Date = datetime.datetime.strptime(CurentDate, "%Y-%m-%d %H:%M:%S")
        order_data = self.w.select(" date, urgency, payment_date ", self.table_name,
                                   " where uid = '{0}' and (id_site = '{1}') ".format(orderid, site_id))[0]
        create_date = order_data.get('date').date()
        urgency = order_data.get('urgency')
        payment_date = order_data.get('payment_date').date()
        client_dl = Date
        writer_dl = Date
        if urgency == '0.12' or urgency == '0':
            client_dl = Date + datetime.timedelta(hours=12)
            writer_dl = Date + datetime.timedelta(hours=9)
        else:
            client_dl = Date + datetime.timedelta(days=int(urgency))
            writer_dl = Date + datetime.timedelta(days=(int(urgency) * 0.75))

        Events().add_event(("UPD DEADLINE - client (date: {0}, urgency: {1}, payment_date: {2})"
                            " new client deadline: {3} "
                            " new writer deadline: {4} ").format(str(create_date), str(urgency), str(payment_date),
                                                                 str(client_dl), str(writer_dl)),
                           self.EVENT_ID_UPD_DEADLINE, orderid, self.SERVICES_ID_SESSION)
        return self.w.update({"wr_deadline": writer_dl, "deadline": client_dl},
                             self.table_name, " where uid='{0}' and (id_site = '{1}') ".format(orderid, site_id))

    def check_orders_limits(self, usid, site_id):
        return self.w.select("count(id)", self.table_name, (" where id_customer='{0}' "
                                                            " and id_order_status=1 "
                                                            " and (id_site = '{1}') ").format(usid, site_id))

    def get_order_rating(self, alr, pages, dl):
        rr = alr + alr * math.sqrt(pages / dl)
        res = 'E'
        if rr >= 15:
            return 'S'
        if 10 <= rr < 15:
            return 'A+'
        if 6 <= rr < 10:
            return 'A'
        if 3 <= rr < 6:
            return 'B'
        if 2 <= rr < 3:
            return 'C'
        if rr < 2:
            return 'D'

    def get_order_to_sms(self, orderid):
        return self.w.select("price,deadline", self.table_name,
                             " where id={0} and (id_site = '{1}') ".format(orderid, self.site_id))

    def get_writer_info_by_order(self, orderid):
        """ This method get info about writer (from table Writers) by Order_UID (from table Orders)
            name: Andrey Kruepnya
            date: 10 12 2015
        """
        return self.w.select(" email,first_name,last_name,phone ", self.table_writers,
                             (" where id=("
                              " select id_writer from {1} "
                              " where lower(uid)=lower('{0}') "
                              " and (id_site = '{2}') "
                              ")").format(orderid, self.table_name, self.site_id))

    def get_all_claim(self, cur_id):
        rez = False
        alldata = self.w.select("*", [self.claimtable],
                                " Where (delflag <> 1) and (ORDER_ID={0}) Order by logtime".format(cur_id))
        return alldata

    def get_text_claim(self, cur_id):
        rez = self.w.select("Sel_CAT", self.claimtable, " Where (ORDER_ID={0}) ".format(cur_id))
        if (not rez is None):
            if (len(rez) > 0):
                return rez[0]['Sel_CAT']
        return None

    def get_desc_claim(self, cur_id):
        rez = self.w.select("DESC_PROBLEM", self.claimtable, " Where (ORDER_ID={0}) ".format(cur_id))
        if (not rez is None):
            if (len(rez) > 0):
                return rez[0]['DESC_PROBLEM']
        return None

    def get_url_claim(self, cur_id):
        rez = self.w.select("DOC_URL", self.claimtable, " Where (ORDER_ID={0}) ".format(cur_id))
        if (not rez is None):
            if (len(rez) > 0):
                return rez[0]['DOC_URL']
        return None

    def add_claim(self, cur_claim):
        return self.w.insert(cur_claim, self.claimtable)

    def upd_claim(self, cur_claim, condition=""):
        return self.w.update(cur_claim, self.claimtable, condition)
