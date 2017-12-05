#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sqlite_wrapper import SQLiteDB
from conf import Conf

class PayPalErr():
    table_name = "paypalerror"

    def __init__(self,App_Root=""):
        self.w = SQLiteDB(App_Root)


  #----------------------- PAYPAL ERROR ---------------------------
    def Get_Sys_LongMsg(self, err_code):
      try:
        rez=self.w.select("long_msg",
                  self.table_name,
                  (" Where (delflag <> 1)  AND " +\
                  " (err_code = '{0}') "+\
                  " ").format(err_code)
                  );
        print rez
        if (rez):
          if (rez[0].get('long_msg')):
            return rez[0].get('long_msg')
      except Exception, e:
        raise
      return None


    def Add_Sys_PayPallErr(self,rec):
      try:
        rez=self.w.insert(rec,self.table_name);
        return rez
      except Exception, e:
        raise
      return False

    def GetAll_Sys_PayPallErr(self):
      try:
        rez=self.w.select("*",
                  self.table_name,
                  " Where (delflag <> 1) ");
        if (rez):
          return rez
      except Exception, e:
        raise
      return None

    def Upd_Sys_Scripts(self, field_id,rec):
      try:
        rez=self.w.update_param(rec, self.table_name, "where (id = '{0}') ".format(field_id))
        return rez
      except Exception, e:
        raise
      return "error"

  #----------------------- END PAYPAL ERROR ---------------------------

