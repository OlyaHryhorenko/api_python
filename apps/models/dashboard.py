from wrapper import Wrapper


class Dashboard():

    table_name_files = "CustomerFiles"
    table_writers_files = "WriterFiles"
    table_name_messages = "MSSupport"

    def __init__(self):
        self.w = Wrapper()

    def get_new_files(self, uid):
        return self.w.select("*", self.table_writers_files, "where status=0 and id_order in (select id from Orders where id_customer={0});".format(uid))

    def get_new_messages(self, uid):
        return self.w.select("*", self.table_name_messages, " as ms left join MSSubject as sb on ms.id_subject = sb.id where ms.id_ms_status=1 and ms.id_customer={0}".format(uid))
