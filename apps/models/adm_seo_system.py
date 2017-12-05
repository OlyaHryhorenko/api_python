#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sqlite_wrapper import SQLiteDB
from conf import Conf

class AdmSeoSystem():
    table_name = "sys_seo"
    table_name_user = "sys_seo_user"

    def __init__(self,App_Root=""):
        self.w = SQLiteDB(App_Root)

#-------------------------- USER SYSTEM --------------------------------
    def Check_User_System(self,lg,ps):
        try:
            rez=self.w.select("id",
                              self.table_name_user,
                              (" Where (Delflag <> 1) AND " +\
                              " (lower(user_) = lower('{0}')) AND"+\
                              " (passw_ = '{1}') "+\
                              " ").format(lg,ps)
                              );
            if (rez):
                if (rez[0].get('id')):
                    return rez[0].get('id')
        except Exception, e:
            raise
        return None


    def Get_User_Passw(self,lg):
        try:
            rez=self.w.select("passw_",
                              self.table_name_user,
                              (" Where (Delflag <> 1) AND " +\
                              " (lower(user_) = lower('{0}')) "+\
                              " ").format(lg)
                              );
            if (rez):
                if (rez[0].get('passw_')):
                    return rez[0].get('passw_')
        except Exception, e:
            print e
            return None
        return None


    def Add_User_System(self,rec):
        try:
            rez=self.w.insert(rec,self.table_name_user);
            return rez
        except Exception, e:
            raise
        return False

    def Del_User_System(self, id_user):
        try:
            rez=self.w.update({"Delflag": 1}, self.table_name_user, " where (id = {0}) ".format(id_user))
            return True
        except Exception, e:
            raise
        return "error"

    def Upd_User_System(self, id_user,sysfield):
        try:
            rez=self.w.update(sysfield, self.table_name_user, " where (id = {0}) ".format(id_user))
            return rez
        except Exception, e:
            raise
        return "error"

    def GetAll_User_System(self):
        try:
            rez=self.w.select("*",
                              self.table_name_user,
                              " Where (Delflag <> 1) ");
            if (rez):
                return rez
        except Exception, e:
            raise
        return None
#---------------------- END USER SYSTEM ---------------------------------

#---------------------- CONSTANTS SYSTEM --------------------------------
    def Upd_Sys_Const(self, field_name,sysfield):
        try:
            rez=self.w.update({"sysfield": sysfield}, self.table_name, "where (namefield = '{0}') ".format(field_name))
            return rez
        except Exception, e:
            raise
        return "error"

    def Del_Sys_Const(self, field_name):
        try:
            rez=self.w.update({"delflag": 1}, self.table_name, "where (namefield = '{0}') ".format(field_name))
            return rez
        except Exception, e:
            raise
        return "error"
#---------------------- END CONSTANTS SYSTEM --------------------------------
