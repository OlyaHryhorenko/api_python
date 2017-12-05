from wrapper import Wrapper
from conf import Conf
from apps.utils.utils import send_mail
from apps.utils.utils import send_mail_from_server
from apps.models.sys_const import SysConst
from apps.models.templateletter import TemlateLetter
import re
import random


class Revisions(object):

    table_rev_categ = "RevisionsCategories"
    table_rev_level = "RevisionsLevels"
    table_rev_status = "RevisionsStatuses"
    table_rev = "Revisions"
#    site_name = 'Pro-Essay-Writer.com'
    site_name = str(SysConst().Get_Sys_Const("site_name"))
    site_name_short = str(site_name).replace('http', '').replace('https', '').replace(':', '').replace('/', '')
#    site_mail = 'support@pro-essay-writer.com'
    site_mail = str(SysConst().Get_Sys_Const("site_mail"))
#    site_pass = '8mdOikTyd0'
    site_pass = str(SysConst().Get_Sys_Const("site_pass"))
#    tsm_mail_address = "noreply@tsm-group.org"
    tsm_mail_address = str(SysConst().Get_Sys_Const("tsm_mail_address"))
#    tsm_mail_pass = "kUG4JnFewyxq"
    tsm_mail_pass = str(SysConst().Get_Sys_Const("tsm_mail_pass"))

    site_noreply_mail = str(SysConst().Get_Sys_Const("noreply_mail"))
    site_noreply_pass = str(SysConst().Get_Sys_Const("noreply_pass"))

    def __init__(self):
        self.w = Wrapper()

    def get_revison_categories(self, cat_id=None):
        try:
            if (cat_id is not None):
                return self.w.select(" id, category ",
                                     self.table_rev_categ,
                                     " where id={0}".format(cat_id)
                                     )
            else:
                return self.w.select(" id, category ",
                                     self.table_rev_categ
                                     )
        except Exception, e:
            print e
        finally:
            pass

    def get_revison_list_categories(self, list_cat_id=None):
        list_categ = ""
        try:
            if (list_cat_id is not None):
                rez = self.w.select(" category ",
                                    self.table_rev_categ,
                                    " where id in ({0}) ".format(list_cat_id)
                                    )
                if rez:
                    if len(rez) > 0:
                        for i in range(len(rez)):
                            list_categ = "{0},{1}".format(rez[i].get('category'),
                                                          list_categ)
                if len(list_categ) > 0:
                    if list_categ[0] == ',':
                        list_categ = list_categ[1:]
                if len(list_categ) > 0:
                    if list_categ[-1:] == ',':
                        list_categ = list_categ[:-1]
                return list_categ
            else:
                return list_categ
        except Exception, e:
            print e
        finally:
            pass

    def get_revison_levels(self, lev_id=None):
        try:
            if (lev_id is not None):
                return self.w.select(" id, level ",
                                     self.table_rev_level,
                                     " where id={0}".format(lev_id)
                                     )
            else:
                return self.w.select(" id, level ",
                                     self.table_rev_level
                                     )
        except Exception, e:
            print e
        finally:
            pass

    def get_revison_status(self, stat_id=None):
        try:
            if (stat_id is not None):
                return self.w.select(" id, status ",
                                     self.table_rev_status,
                                     " where id={0}".format(stat_id)
                                     )
            else:
                return self.w.select(" id, status ",
                                     self.table_rev_categ
                                     )
        except Exception, e:
            print e
        finally:
            pass

    def add_revisiov(self, cur_rev):
        return self.w.insert(cur_rev, self.table_rev)

    def upd_revisiov(self, cur_rev, condition=""):
        return self.w.update(cur_rev, self.table_rev, condition)
