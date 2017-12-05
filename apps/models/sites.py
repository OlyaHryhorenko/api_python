from wrapper import Wrapper


class Sites(object):

    def __init__(self, wrapper):
        if wrapper is None:
            raise TypeError

        self.w = wrapper
        self.NAME = 'Sites'

    def get_all(self):
        return self.w.select("SQL_CACHE *", self.NAME)

    def add_site(self, fields):
        return self.w.insert(fields, self.NAME)

    def get_site(self, id):
        return self.w.select(["*"], self.NAME, "where id=%s" % id)

    def edit_site(self, fields, condition):
        return self.w.update(fields, self.NAME, condition)

    def change_status(self, status, id):
        self.w.update({"status": status}, self.NAME, "where id=%s" % id)

    def update_orders(self, orders, last_order, id):
        self.w.update({"orders": orders, "last_order": last_order}, self.NAME, "where id=%s" % id)

    def check_site(self, site):
        return self.w.select(["id"], self.NAME, 'where site="%s"' % site)