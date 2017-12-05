#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sqlite_wrapper import SQLiteDB
from conf import Conf

class Prices():
	table_name = "prices"
	table_name_spc_kof = "pricespace"

	def __init__(self,App_Root=""):
		self.w = SQLiteDB(App_Root)


	def Add_Price_For_Work(self,rec):
		try:
			rez=self.w.insert_param(rec,self.table_name);
			return rez
		except Exception, e:
			raise
		return False

	def Upd_Price_For_Work(self, field_id,rec):
		try:
			rez=self.w.update_param(rec, self.table_name, "where (id = '{0}') ".format(field_id))
			return rez
		except Exception, e:
			raise
		return "error"

	def Del_Price_For_Work(self, field_id):
		try:
			rez=self.w.update({"delflag": 1}, self.table_name, "where (id = '{0}') ".format(field_id))
			return rez
		except Exception, e:
			raise
		return "error"

	def GetAll_Price_For_Work(self,type_price):
		try:
			rez=self.w.select("*",
							  self.table_name,
							  " Where (Delflag <> 1) and (id_table = '{0}') Order by id_table,format,urgenc,datefrom".format(type_price));
			if (rez):
				return rez
		except Exception, e:
			raise
		return None

	def Get_Price_For_Work(self, id_table, frmt,urgenc,spc,pgs):
		try:
			rez=self.w.select("price",
							  self.table_name,
							  (" Where (Delflag <> 1) AND " +\
							  " (id_table = {0}) AND"+\
							  " (format = {1}) AND"+\
							  " ( {2} <= urgenc )"+\
							  " Order BY urgenc ASC, datefrom DESC Limit 1 ").format(id_table,frmt,urgenc)
							  );
			if (rez):
				if (rez[0].get('price')):
					price_without_discount=float(rez[0].get('price'))*float(spc)*float(pgs)
					return price_without_discount
		except Exception, e:
			raise
		return None

	def Get_Price_For_Work_JSON(self, cur_date):
		try:
			rez=self.w.select(" id_table, format, urgenc, price ",
							  self.table_name,
							  (" as pr Where  " +\
							  " pr.datefrom = (select MAX(pr_2.datefrom) from "+self.table_name+" as pr_2 "+\
							  " where "+\
							  " (pr.id_table=pr_2.id_table) AND "+\
							  " (pr.format=pr_2.format) AND "+\
							  " (pr.urgenc=pr_2.urgenc) AND "+\
							  " (pr_2.delflag=0) AND "+\
							  " (pr_2.datefrom<='{0}') ) AND "+\
							  " pr.delflag=0  "+\
							  " Order by  "+\
							  " id_table, format, urgenc, price ").format(cur_date)
							  );
			if (rez):
				return rez
		except Exception, e:
			raise
		return None

	def Get_Kof_Count_Space_JSON(self, cur_date):
		try:
			rez=self.w.select(" countspace, kof ",
							  self.table_name_spc_kof,
							  (" as pr Where  " +\
							  " pr.datefrom = (select MAX(pr_2.datefrom) from "+self.table_name_spc_kof+" as pr_2 "+\
							  " where "+\
							  " (pr.countspace=pr_2.countspace) AND "+\
							  " (pr.kof=pr_2.kof) AND "+\
							  " (pr_2.delflag=0) AND "+\
							  " (pr_2.datefrom<='{0}') ) AND "+\
							  " pr.delflag=0  "+\
							  " Order by  "+\
							  " countspace, kof ").format(cur_date)
							  );
			if (rez):
				return rez
		except Exception, e:
			raise
		return 1

	def Get_Kof_Count_Space(self, cnt_spc):
		try:
			rez=self.w.select("kof",
							  self.table_name_spc_kof,
							  (" Where (Delflag <> 1) AND " +\
							  " (countspace = {0}) "+\
							  " Order By datefrom DESC Limit 1 ").format(cnt_spc)
							  );
			if (rez):
				if (rez[0].get('kof')):
					kof=float(rez[0].get('kof'))
					return kof
		except Exception, e:
			raise
		return 1

