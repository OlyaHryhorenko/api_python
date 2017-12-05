from wrapper import Wrapper


class Messages():

    table_name = "MSCustomers"
    table_name2 = "MSSupport"
    subject_table = "MSSubject"

    html_escape_table = {"&": "&amp;", '"': "&quot;", "'": "&apos;",
                         ">": "&gt;", "<": "&lt;"}

    def __init__(self):
        self.w = Wrapper()

    def html_escape(self, text):
        return "".join(self.html_escape_table.get(c, c) for c in text)

    def send_subject(self, subject, orderid):
        return self.w.insert({"subject": subject, "id_order": orderid},
                             self.subject_table)

    def send_subject_noid(self, subject):
        return self.w.insert({"subject": subject}, self.subject_table)

    def send_message(self, date, subjectid, message, fpath, id_customer):
        return self.w.insert({"date": date, "id_subject": subjectid,
                              "message": message, "fpath": fpath,
                              "id_customer": id_customer, "id_ms_status": 1},
                             self.table_name)

    def send_message_nofile(self, date, subjectid, message, id_customer):
        return self.w.insert({"date": date, "id_subject": subjectid,
                              "message": message, "id_customer": id_customer,
                              "id_ms_status": 1}, self.table_name)

    def get_user_messages_by_order(self, oderid):
        return self.w.select("*", self.table_name, "where id_order={0}".format(oderid))

    def get_user_messages_by_order2(self, oderid):
        return self.w.select("*", self.table_name + " as m left join MSSubject as s on m.id_subject = s.id where id_order={0} order by m.date".format(oderid))

    def get_support_messages_by_order(self, oderid):
        return self.w.select("*", self.table_name2, "where id_order={0}".format(oderid))

    def get_all_support_messages_by_user(self, uid):
        return self.w.select("id", self.table_name, "where id_customer={0}".format(uid))

    def get_new_support_messages_by_uid(self, uid):
        self.message_from_support = self.w.select("*", self.table_name,
                                                  "where id_customer={0} and id_status=1".format(uid))
        return self.message_from_support

    def get_support_messages_by_id(self, mid):
        return self.w.select("*", self.table_name2, "where id={0}".format(mid))

    def get_all_message(self, oderid):
        return self.w.select("date,message,fpath,id_customer,id_subject,id_ms_status,subject", self.table_name + " as c left join MSSubject as s on c.id_subject = s.id where id_order={0} union select date,message,fpath,id_customer,id_subject,id_ms_status,subject from MSSupport as ss left join MSSubject as s on ss.id_subject = s.id where id_order={0} order by date DESC".format(oderid))
