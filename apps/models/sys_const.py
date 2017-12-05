#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sqlite_wrapper import SQLiteDB
from conf import Conf


class SysConst():
    table_name = "sys_const"
    table_header = "sys_header"
    table_footer = "sys_footer"
    table_loginform = "sys_loginform"
    table_scripts = "sys_scripts"
    table_blog = "sys_blog"
    table_links = "sys_links"
    table_links_template = "sys_links_template"
    table_sitemap = "sys_sitemap"

    def __init__(self, App_Root=""):
        self.w = SQLiteDB(App_Root)

    # ----------------------- SYSTEM CONSTANT ---------------------------
    def Get_Sys_Const(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_name,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') " +
                                 " ").format(field_name)
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            raise
        return None

    def Add_Sys_Const(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_name)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Const(self):
        try:
            rez = self.w.select("*",
                                self.table_name,
                                " Where (Delflag <> 1) ")
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Const(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_name, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            raise
        return "error"

    def Del_Sys_Const(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_name, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END SYSTEM CONSTANT ---------------------------

    # ----------------------- SYSTEM HEADER ---------------------------
    def Get_Sys_Header(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_header,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') " +
                                 " ").format(field_name)
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_Header(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_header)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Header(self):
        try:
            rez = self.w.select("*",
                                self.table_header,
                                " Where (Delflag <> 1) ")
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Header(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_header, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_Header(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_header, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END SYSTEM HEADER ---------------------------


    # ----------------------- SYSTEM FOOTER ---------------------------
    def Get_Sys_Footer(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_footer,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') " +
                                 " ").format(field_name)
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_Footer2(self, rec):
        try:
            rez = self.w.insert(rec, self.table_footer)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def Add_Sys_Footer(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_footer)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Footer(self):
        try:
            rez = self.w.select("*",
                                self.table_footer,
                                " Where (Delflag <> 1) ")
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Footer(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_footer, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_Footer(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_footer, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END SYSTEM FOOTER ---------------------------

    # ----------------------- SYSTEM LOGINFORM ---------------------------
    def Get_Sys_Loginform(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_loginform,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') " +
                                 " ").format(field_name)
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_Loginform(self, rec):
        try:
            rez = self.w.insert(rec, self.table_loginform)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def Add_Sys_Loginform(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_loginform)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Loginform(self):
        try:
            rez = self.w.select("*",
                                self.table_loginform,
                                " Where (Delflag <> 1) ")
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Loginform(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_loginform, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_Loginform(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_loginform, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END SYSTEM LOGINFORM ---------------------------


    # ----------------------- SYSTEM SCRIPTS ---------------------------
    def Get_Sys_Scripts(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_scripts,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') " +
                                 " ").format(field_name)
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_Scripts(self, rec):
        try:
            rez = self.w.insert(rec, self.table_scripts)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def Add_Sys_Scripts(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_scripts)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Scripts(self):
        try:
            rez = self.w.select("*",
                                self.table_scripts,
                                " Where (Delflag <> 1) ")
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Scripts(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_scripts, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_Scripts(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_scripts, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END SYSTEM SCRIPTS ---------------------------

    # ----------------------- SYSTEM BLOG ---------------------------
    def Get_Sys_Blog(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') AND " +
                                 " (idpage = '{1}') " +
                                 " ").format(field_name, "7")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_Blog(self, rec):
        try:
            rez = self.w.insert(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def Add_Sys_Blog(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Blog(self):
        try:
            rez = self.w.select(" sb.*, sl.namefield as namefield2, sl.sysfield as sysfield2 ",
                                self.table_blog,
                                ("as sb left join" +
                                 " " + self.table_links + " as sl" +
                                 " ON sl.id=sb.idlinks" +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage = '{0}') " +
                                 " ").format("7")
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def GetHTML_Sys_Blog(self, content_url, type_content="h"):
        try:
            cnt_to = "%head%"
            if (type_content == "b"):
                cnt_to = "%body%"
            rez = self.w.select(" sb.sysfield as sf",
                                self.table_blog,
                                ("as sb left join" +
                                 " " + self.table_links + " as sl" +
                                 " ON sl.id=sb.idlinks" +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage = '{0}')  AND " +
                                 " (sl.sysfield = '{1}')  AND " +
                                 " (sb.namefield like '{2}')  " +
                                 " ").format("7", content_url, cnt_to)
                                )
            if (rez):
                if (rez[0].get('sf')):
                    return rez[0].get('sf')
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Blog(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_Blog(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END SYSTEM BLOG ---------------------------


    # ----------------------- ALL OTHER PAGES ---------------------------
    def Get_Sys_Other_Pages(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') AND " +
                                 " (idpage = '{1}') " +
                                 " ").format(field_name, "0")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_Other_Pages(self, rec):
        try:
            rez = self.w.insert(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def Add_Sys_Other_Pages(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Other_Pages(self):
        try:
            rez = self.w.select(" sb.*, sl.namefield as namefield2, sl.sysfield as sysfield2 ",
                                self.table_blog,
                                ("as sb left join" +
                                 " " + self.table_links + " as sl" +
                                 " ON sl.id=sb.idlinks" +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage = '{0}') " +
                                 " ").format("0")
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def GetHTML_Sys_Other_Pages(self, content_url, type_content="h"):
        try:
            cnt_to = "%head%"
            if (type_content == "b"):
                cnt_to = "%body%"
            rez = self.w.select(" sb.sysfield as sf",
                                self.table_blog,
                                ("as sb left join" +
                                 " " + self.table_links + " as sl" +
                                 " ON sl.id=sb.idlinks" +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage = '{0}')  AND " +
                                 " (sl.sysfield = '{1}')  AND " +
                                 " (sb.namefield like '{2}')  " +
                                 " ").format("0", content_url, cnt_to)
                                )
            if (rez):
                if (rez[0].get('sf')):
                    return rez[0].get('sf')
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Other_Pages(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_Other_Pages(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END ALL OTHER PAGES ---------------------------

    # ----------------------- SYSTEM LINKS ---------------------------
    def Get_Sys_Links(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_links,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') " +
                                 " ").format(field_name)
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_Links(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_links)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Links(self):
        try:
            rez = self.w.select("*",
                                self.table_links_template,
                                " Where (Delflag <> 1) ")
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Links(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_links, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_Links(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_links, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END SYSTEM LINKS ---------------------------

    # ----------------------- Page About ---------------------------
    def Get_Sys_About(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') AND " +
                                 " (idpage = '{1}') " +
                                 " ").format(field_name, "0")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    # ----------------------- END ABOUT LINKS ---------------------------

    # ----------------------- Page Index ---------------------------
    def Get_Sys_Index(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') AND " +
                                 " (idpage = '{1}') " +
                                 " ").format(field_name, "1")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_Index(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Index(self):
        try:
            rez = self.w.select("*",
                                self.table_blog,
                                " Where (Delflag <> 1) and (idpage=1) ")
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Index(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_Index(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END Page Index ---------------------------

    # ----------------------- Page Prices ---------------------------
    def Get_Sys_Prices(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') AND " +
                                 " (idpage = '{1}') " +
                                 " ").format(field_name, "2")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_Prices(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Prices(self):
        try:
            rez = self.w.select("*",
                                self.table_blog,
                                " Where (Delflag <> 1) and (idpage=2) ")
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Prices(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_Prices(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END Page Prices ---------------------------

    # ----------------------- Page Howitworks ---------------------------
    def Get_Sys_Howitworks(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') AND " +
                                 " (idpage = '{1}') " +
                                 " ").format(field_name, "3")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_Howitworks(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Howitworks(self):
        try:
            rez = self.w.select("*",
                                self.table_blog,
                                " Where (Delflag <> 1) and (idpage=3) ")
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Howitworks(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_Howitworks(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END Page Howitworks ---------------------------

    # ----------------------- Page Samples ---------------------------
    def Get_Sys_Samples(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') AND " +
                                 " (idpage = '{1}') " +
                                 " ").format(field_name, "4")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_Samples(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Samples(self):
        try:
            rez = self.w.select("*",
                                self.table_blog,
                                " Where (Delflag <> 1) and (idpage=4) ")
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Samples(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_Samples(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END Page Samples ---------------------------

    # ----------------------- Page Contacts ---------------------------
    def Get_Sys_Contacts(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') AND " +
                                 " (idpage = '{1}') " +
                                 " ").format(field_name, "5")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_Contacts(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_Contacts(self):
        try:
            rez = self.w.select("*",
                                self.table_blog,
                                " Where (Delflag <> 1) and (idpage=5) ")
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_Contacts(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_Contacts(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END Page Contacts ---------------------------

    # ----------------------- Page FAQ ---------------------------
    def Get_Sys_FAQ(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}') AND " +
                                 " (idpage = '{1}') " +
                                 " ").format(field_name, "6")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Sys_FAQ(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Sys_FAQ(self):
        try:
            rez = self.w.select("*",
                                self.table_blog,
                                " Where (Delflag <> 1) and (idpage=6) ")
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Sys_FAQ(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Sys_FAQ(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END Page FAQ ---------------------------


    # ----------------------- GET LIST CONTENT INTO PAGES ---------------------------
    def Get_Content_by_fildname_Pages(self, field_name, id_link):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}')  AND " +
                                 " (idpage = '{1}') AND " +
                                 " (idlinks = '{2}') " +
                                 " ORDER BY id").format(field_name, "20", id_link)
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Content_Pages(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Content_Pages(self):
        try:
            rez = self.w.select(
                " sb.*, lt.namefield as namefield2, lt.urlfield as sysfield2, lt.templfield as templfield ",
                self.table_blog,
                ("as sb left join" +
                 " " + self.table_links_template + " as lt" +
                 " ON lt.id=sb.idlinks" +
                 " Where (sb.delflag <> 1)  AND " +
                 " (sb.idpage = '{0}') " +
                 " ORDER BY sb.id").format("20")
                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def GetAll_Content_Pages_By_Id(self, id_link):
        try:
            rez = self.w.select(
                " sb.*, lt.namefield as namefield2, lt.urlfield as sysfield2, lt.templfield as templfield ",
                self.table_blog,
                ("as sb left join" +
                 " " + self.table_links_template + " as lt" +
                 " ON lt.id=sb.idlinks" +
                 " Where (sb.delflag <> 1)  AND " +
                 " (sb.idlinks = '{0}')  AND " +
                 " (sb.idpage = '{1}') " +
                 " ORDER BY sb.id").format(id_link, "20")
                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def GetHTML_Content_Pages(self, content_url):
        try:
            rez = self.w.select(" sb.sysfield as sf, sb.namefield as nf",
                                self.table_blog,
                                ("as sb left join" +
                                 " " + self.table_links_template + " as tl" +
                                 " ON tl.id=sb.idlinks" +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage = '{0}')  AND " +
                                 " (tl.urlfield in ({1}) ) " +
                                 " ORDER BY sb.id").format("20", content_url)
                                )
            if (rez):
                content = {}
                for i in range(len(rez)):
                    if (rez[i].get('sf')):
                        # ##content.append(rez[i].get('sf'))
                        content[rez[i].get('nf')] = rez[i].get('sf')
                return content
            else:
                return None
        except Exception, e:
            print e
            raise
        return None

    def Upd_Content_Pages(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Content_Pages(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Content_Pages_by_Tag(self, field_id_link, name):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, (" where (idlinks = {0}) " +
                                                                  " and (namefield= '{1}') " +
                                                                  " and (Delflag = 0) " +
                                                                  " and (idpage = '{2}') ").format(field_id_link, name,
                                                                                                   "20"))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END LIST CONTENT INTO PAGES ---------------------------


    # ----------------------- GET LIST CONTENT INTO BLOG ---------------------------
    def Get_Blog_Content_by_fildname_Pages(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}')  AND " +
                                 " (idpage = '{1}') " +
                                 " ORDER BY id").format(field_name, "30")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Blog_Content_Pages(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Blog_Content_Pages(self):
        try:
            rez = self.w.select(" sb.*, sl.namefield as namefield2, sl.sysfield as sysfield2 ",
                                self.table_blog,
                                ("as sb left join" +
                                 " " + self.table_links + " as sl" +
                                 " ON sl.id=sb.idlinks" +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage = '{0}') " +
                                 " ORDER BY sb.id").format("30")
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def GetHTML_Blog_Content_Pages(self, content_url):
        try:
            rez = self.w.select(" sb.sysfield as sf, sb.namefield as nf",
                                self.table_blog,
                                ("as sb left join" +
                                 " " + self.table_links + " as sl" +
                                 " ON sl.id=sb.idlinks" +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage = '{0}')  AND " +
                                 " (sl.sysfield = '{1}') " +
                                 " ORDER BY sb.id").format("30", content_url)
                                )
            if (rez):
                content = {}
                for i in range(len(rez)):
                    if (rez[i].get('sf')):
                        # ##content.append(rez[i].get('sf'))
                        content[rez[i].get('nf')] = rez[i].get('sf')
                return content
            else:
                return None
        except Exception, e:
            print e
            raise
        return None

    def Upd_Blog_Content_Pages(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Blog_Content_Pages(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END LIST CONTENT INTO BLOG --------------------------


    # ----------------------- GET LIST CONTENT INTO INCLUDE PAGE ------------------
    def Get_Include_Content_by_fildname_Pages(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}')  AND " +
                                 " (idpage in ({1}) ) " +
                                 " ORDER BY id").format(field_name, "40,70")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            raise
        return None

    def Add_Include_Content_Pages(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Include_Content_Pages(self):
        try:
            rez = self.w.select(" sb.* ",
                                self.table_blog,
                                (" as sb " +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage in ({0}) ) " +
                                 " ORDER BY sb.id").format("40,70")
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def GetHTML_Include_Content_Pages(self):
        try:
            rez = self.w.select(" sb.sysfield as sf, sb.namefield as nf",
                                self.table_blog,
                                (" as sb " +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage in ({0})  ) " +
                                 " ORDER BY sb.id").format("40,70")
                                )
            if (rez):
                content = {}
                for i in range(len(rez)):
                    if (rez[i].get('sf')):
                        # ##content.append(rez[i].get('sf'))
                        content[rez[i].get('nf')] = rez[i].get('sf')
                return content
            else:
                return None
        except Exception, e:
            print e
            raise
        return None

    def Upd_Include_Content_Pages(self, field_id, rec):
        try:
            rez = self.w.update_param(rec,
                                      self.table_blog,
                                      "where (id = '{0}') ".format(field_id)
                                      )
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Include_Content_Pages(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1},
                                self.table_blog,
                                "where (id = {0}) ".format(field_id)
                                )
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Include_Content_Pages_By_Name(self, field_name):
        try:
            rez = self.w.update({"Delflag": 1},
                                self.table_blog,
                                "where (idpage in ({0}) ) AND (namefield='{1}') AND (Delflag <> 1) ".format("40,70",
                                                                                                            field_name)
                                )
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END LIST CONTENT INTO INCLUDE PAGE ------------------

    # ----------------------- GET LIST TEMPLATE PAGES ---------------------------
    def Get_Template_by_fildname_Pages(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}')  AND " +
                                 " (idpage = '{1}') " +
                                 " ORDER BY id").format(field_name, "50")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            print e
            raise
        return None

    def Add_Template_Pages(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Template_Pages(self):
        try:
            rez = self.w.select(" sb.*, sl.namefield as namefield2, sl.sysfield as sysfield2 ",
                                self.table_blog,
                                ("as sb left join" +
                                 " " + self.table_links + " as sl" +
                                 " ON sl.id=sb.idlinks" +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage = '{0}') " +
                                 " ORDER BY sb.id").format("50")
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Get_Template_Pages_Old(self, content_url):
        try:
            rez = self.w.select(" sb.sysfield as sf",
                                self.table_blog,
                                ("as sb left join" +
                                 " " + self.table_links + " as sl" +
                                 " ON sl.id=sb.idlinks" +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage = '{0}')  AND " +
                                 " (sl.sysfield = '{1}') " +
                                 " ORDER BY sb.id").format("50", content_url)
                                )
            if (rez):
                if (rez[0].get('sf')):
                    return rez[0].get('sf')
            else:
                return None
        except Exception, e:
            print e
            raise
        return None

    def Get_Template_Pages(self, content_url):
        try:
            rez = self.w.select(" lt.templfield as tf",
                                self.table_links_template,
                                ("as lt " +
                                 " Where (lt.Delflag <> 1)  AND " +
                                 " (lt.urlfield in ({0}) ) " +
                                 " ORDER BY lt.id").format(content_url)
                                )
            if (rez):
                if (rez[0].get('tf')):
                    return rez[0].get('tf')
            else:
                return None
        except Exception, e:
            print e
            raise
        return None

    def Upd_Template_Pages(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Template_Pages(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END LIST TEMPLATE PAGES ---------------------------

    # ----------------------- GET LIST Link & Template ---------------------------
    def Get_Link_Template(self, field_name):
        try:
            rez = self.w.select("id, urlfield, templfield, comment",
                                self.table_links_template,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}')  AND " +
                                 " ORDER BY id").format(field_name)
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Get_Link_Template(self, field_id):
        try:
            rez = self.w.select("namefield, urlfield, templfield, comment",
                                self.table_links_template,
                                (" Where (Delflag <> 1) AND " +
                                 " (id = '{0}')  AND " +
                                 " ORDER BY id").format(field_id)
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Add_Link_Template(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_links_template)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Link_Template(self):
        try:
            rez = self.w.select("id, namefield, urlfield, templfield, comment",
                                self.table_links_template,
                                (" Where (Delflag <> 1)" +
                                 " ORDER BY id")
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def GetNamefield_Link_Template(self, content_url):
        try:
            rez = self.w.select("namefield, templfield, comment",
                                self.table_links_template,
                                (" Where (Delflag <> 1) AND " +
                                 " (urlfield = '{0}')  AND " +
                                 " ORDER BY id").format(content_url)
                                )
            if (rez):
                return rez
            else:
                return None
        except Exception, e:
            print e
            raise
        return None

    def Upd_Link_Template(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_links_template, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Link_Template(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_links_template, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END LIST Link & Template -----------------------------------

    # ----------------------- GET LIST MENU ITEMS HEADER ---------------------------
    def Add_Menu_Items_Header(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def Get_Max_Id(self):
        try:
            rez = self.w.select(" MAX(id) as id ",
                                self.table_blog, ""
                                )
            if (rez):
                if (rez[0].get('id')):
                    return rez[0].get('id')
        except Exception, e:
            print e
            raise
        return None

    def GetAll_Menu_Items_Header(self):
        try:
            rez = self.w.select(" sb.*, slt.namefield as namefield2, slt.urlfield ",
                                self.table_blog,
                                (" as sb left join " +
                                 " " + self.table_links_template + " as slt " +
                                 " ON slt.id=sb.idlinks " +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage = '{0}') " +
                                 " ORDER BY sb.sysfield").format("60")
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Get_Menu_Items_Header_Order(self, field_id, order_by="cur"):
        try:
            ord_b = " ASC "
            filter_id = " (sysfield = '{}') ".format(field_id)
            if (order_by == "up"):
                filter_id = " (sysfield < '{}') ".format(field_id)
                ord_b = " DESC "
            elif (order_by == "down"):
                filter_id = " (sysfield > '{}') ".format(field_id)
            rez = self.w.select(" id, sysfield ",
                                self.table_blog,
                                (" Where (delflag <> 1)  AND " +
                                 " (idpage = '{0}') AND {1} " +
                                 " ORDER BY sysfield {2}  limit 1 ").format("60", filter_id, ord_b)
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Menu_Items_Header(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Menu_Items_Header(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END LIST MENU ITEMS HEADER ---------------------------


    # ----------------------- GET LIST MENU ITEMS FOOTER ---------------------------
    def Add_Menu_Items_Footer(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Menu_Items_Footer(self):
        try:
            rez = self.w.select(" sb.*, slt.namefield as namefield2, slt.urlfield ",
                                self.table_blog,
                                ("as sb left join" +
                                 " " + self.table_links_template + " as slt" +
                                 " ON slt.id=sb.idlinks" +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage = '{0}') " +
                                 " ORDER BY sb.sysfield").format("65")
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Get_Menu_Items_Footer_Order(self, field_id, order_by="cur"):
        try:
            ord_b = " ASC "
            filter_id = " (sysfield = '{}') ".format(field_id)
            if (order_by == "up"):
                filter_id = " (sysfield < '{}') ".format(field_id)
                ord_b = " DESC "
            elif (order_by == "down"):
                filter_id = " (sysfield > '{}') ".format(field_id)
            rez = self.w.select(" id, sysfield ",
                                self.table_blog,
                                (" Where (delflag <> 1)  AND " +
                                 " (idpage = '{0}') AND {1} " +
                                 " ORDER BY sysfield {2}  limit 1 ").format("65", filter_id, ord_b)
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Menu_Items_Footer(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Menu_Items_Footer(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END LIST MENU ITEMS FOOTER ---------------------------

    # ----------------------- GET LIST SITEBAR CONTENT ---------------------------
    def Get_Content_Sitebar_by_fildname(self, field_name):
        try:
            rez = self.w.select("sysfield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (namefield = '{0}')  AND " +
                                 " (idpage = '{1}') " +
                                 " ORDER BY id").format(field_name, "70")
                                )
            if (rez):
                if (rez[0].get('sysfield')):
                    return rez[0].get('sysfield')
        except Exception, e:
            raise
        return None

    def Get_Content_Sitebar_by_id(self, field_id):
        try:
            rez = self.w.select("namefield",
                                self.table_blog,
                                (" Where (Delflag <> 1) AND " +
                                 " (id = '{0}')  AND " +
                                 " (idpage = '{1}') " +
                                 " ORDER BY id").format(field_id, "70")
                                )
            if (rez):
                if (rez[0].get('namefield')):
                    return rez[0].get('namefield')
        except Exception, e:
            raise
        return None

    def Add_Content_Sitebar(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_blog)
            return rez
        except Exception, e:
            print e
            raise
        return False

    def GetAll_Content_Sitebar(self):
        try:
            rez = self.w.select(" sb.* ",
                                self.table_blog,
                                (" as sb " +
                                 " Where (sb.delflag <> 1)  AND " +
                                 " (sb.idpage = '{0}') " +
                                 " ORDER BY sb.id").format("70")
                                )
            if (rez):
                return rez
        except Exception, e:
            print e
            raise
        return None

    def Upd_Content_Sitebar(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_blog, " where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Content_Sitebar(self, field_id):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog, " where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    def Del_Content_Sitebar_By_Name(self, field_name):
        try:
            rez = self.w.update({"Delflag": 1}, self.table_blog,
                                " where (idpage = {0}) AND (namefield='{1}') AND (Delflag <> 1) ".format("70",
                                                                                                         field_name))
            return rez
        except Exception, e:
            print e
            raise
        return "error"

    # ----------------------- END LIST SITEBAR CONTENT --------------------------

    # ----------------------- SYSTEM SITEMAP ---------------------------
    def Get_Sys_Sitemap(self, field_name):
        try:
            rez = self.w.select("changefreq, priority",
                                self.table_sitemap,
                                (" Where (delflag <> 1) AND " +
                                 " (loc = '{0}') " +
                                 " ").format(field_name)
                                )
            if (rez):
                if (len(rez) > 0):
                    return rez
        except Exception, e:
            raise
        return None

    def Add_Sys_Sitemap(self, rec):
        try:
            rez = self.w.insert_param(rec, self.table_sitemap)
            return rez
        except Exception, e:
            raise
        return False

    def GetAll_Sys_Sitemap(self):
        try:
            rez = self.w.select(" ss.id, ss.loc, ss.changefreq, ss.priority, sl.namefield, sl.urlfield ",
                                self.table_sitemap,
                                " as ss " + \
                                " left join " + \
                                " {} as sl".format(self.table_links_template) + \
                                " ON sl.id=ss.loc " + \
                                " Where (ss.delflag <> 1) " + \
                                " Order by ss.priority desc, ss.loc ")
            if (rez):
                return rez
        except Exception, e:
            raise
        return None

    def Upd_Sys_Sitemap(self, field_id, rec):
        try:
            rez = self.w.update_param(rec, self.table_sitemap, "where (id = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            raise
        return "error"

    def Del_Sys_Sitemap(self, field_id):
        try:
            rez = self.w.update({"delflag": 1}, self.table_sitemap, "where (id = {0}) ".format(field_id))
            return rez
        except Exception, e:
            raise
        return "error"

    def Del_Sys_Sitemap_by_Url(self, field_id):
        try:
            rez = self.w.update({"delflag": 1}, self.table_sitemap, "where (loc = '{0}') ".format(field_id))
            return rez
        except Exception, e:
            raise
        return "error"

        # ----------------------- END SYSTEM SITEMAP ---------------------------
