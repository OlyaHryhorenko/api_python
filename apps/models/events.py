from wrapper import Wrapper
from time import gmtime, strftime


class Events(object):

    table_name = "Events"

    def __init__(self):
        self.w = Wrapper()

    def add_event(self, description, id_event_type, id_order, id_customer):
        curdate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return self.w.insert({"description": description, "date": curdate,
                              "id_event_type": id_event_type, "id_order": id_order,
                              "id_customer": id_customer}, self.table_name)

    def add_event_no_order(self, description, id_event_type, id_customer):
        curdate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return self.w.insert({"description": description, "date": curdate,
                              "id_event_type": id_event_type, "id_customer": id_customer},
                             self.table_name)
