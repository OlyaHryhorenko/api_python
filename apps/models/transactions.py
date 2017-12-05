from wrapper import Wrapper
from conf import Conf


class Transactions(object):
    def __init__(self):
        self.w = Wrapper()

    table_name = 'CPayments'

    def add_transactions(self, email, fname, lname, date, token, pid, ccode, cstatus, order_id, customer_id,
                         trans_id="-1"):
        return self.w.insert(
            {"email": email, "first_name": fname, "last_name": lname, "date": date, "token": token, "payer_id": pid,
             "country_code": ccode, "check_out_status": cstatus, "id_order": order_id, "id_customer": customer_id,
             "trans_id": trans_id}, self.table_name)

    def get_transactions(self, userid):
        return self.w.select(
            "cp.date,o.uid,cp.check_out_status,o.price,cp.id_customer,cp.trans_id", self.table_name,
            " AS cp LEFT JOIN Orders AS o ON cp.id_order = o.id where cp.id_customer={0} and o.id_order_status > 1 group by o.uid".format(
                userid))

        # SELECT *  FROM  `CPayments` AS cp LEFT JOIN Orders AS o ON cp.id_order = o.id
