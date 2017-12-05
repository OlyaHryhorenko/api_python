#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sqlite3
from conf import Conf


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLiteDB():
    """SQLite wrapper"""

    def __init__(self, dbfile=""):
        if (dbfile == ""):
            App_Root = os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)), os.pardir))
            dbfile = os.path.join(App_Root, Conf("SqLite").read_sqlite())
        else:
            dbfile = os.path.join(dbfile, Conf("SqLite").read_sqlite())
        self.dbfile = dbfile

    def select(self, columns, table_names, condition=""):
        if not isinstance(table_names, basestring):
            table_names = ", ".join(table_names)

        if not isinstance(columns, basestring):
            columns = ", ".join(columns)

        conn = sqlite3.connect(self.dbfile)
        conn.text_factory = str
        conn.row_factory = dict_factory

        try:
            # ##print "select {0} from {1} {2}".format(columns, table_names, condition)
            cursor = conn.execute("select {0} from {1} {2}".format(columns, table_names, condition))
            return cursor.fetchall()
        except Exception, err:
            return err
        finally:
            conn.close()

    def select_old(self, columns, table_names, condition=""):
        if not isinstance(table_names, basestring):
            table_names = ", ".join(table_names)

        if not isinstance(columns, basestring):
            columns = ", ".join(columns)

        conn = sqlite3.connect(self.dbfile)
        conn.text_factory = str

        try:
            cursor = conn.execute("select {0} from {1} {2}".format(columns, table_names, condition))
            return cursor.fetchall()
        except Exception, err:
            return err
        finally:
            conn.close()

    def selectiduser(self, columns, table_names, condition_usr="", condition_psw=""):
        if not isinstance(table_names, basestring):
            table_names = ", ".join(table_names)

        if not isinstance(columns, basestring):
            columns = ", ".join(columns)

        conn = sqlite3.connect(self.dbfile)
        conn.text_factory = str

        try:
            cursor = conn.execute("select {0} from {1} Where S_USER=? AND PASSW=?".format(columns, table_names), (condition_usr, condition_psw))
            return cursor.fetchall()
        except Exception, err:
            return err
        finally:
            conn.close()

    def insert(self, diction, table_name):
        if isinstance(diction, dict):
            keys = ", ".join("{}".format(key) for key in diction)
            values = ", ".join("'{}'".format(diction[key]) for key in diction)
            diction = "({0}) values ({1})".format(keys, values)

        conn = sqlite3.connect(self.dbfile)
        conn.text_factory = str

        try:
            cursor = conn.execute("insert into {0} {1}".format(table_name, diction))
            conn.commit()
            return cursor.lastrowid
        except Exception, err:
            return err
        finally:
            conn.close()

    def insert_param(self, diction, table_name):
        args = []
        if isinstance(diction, dict):
            keys = ", ".join("{}".format(key) for key in diction)
            values = ", ".join("?" for key in diction)
            for key in diction:
                args.append(diction[key])
            diction = "({0}) values ({1})".format(keys, values)

        conn = sqlite3.connect(self.dbfile)
        conn.text_factory = str

        try:
            cursor = conn.execute("insert into {0} {1}".format(table_name, diction), args)
            conn.commit()
            return cursor.lastrowid
        except Exception, err:
            return err
        finally:
            conn.close()

    def update(self, diction, table_names, condition=""):
        if not isinstance(table_names, basestring):
            table_names = ", ".join(table_names)

        if isinstance(diction, dict):
            diction = ", ".join("{}='{}'".format(k, v) for k, v in diction.items())

        conn = sqlite3.connect(self.dbfile)
        conn.text_factory = str

        try:
            cursor = conn.execute("update {0} set {1} {2}".format(table_names, diction, condition))
            conn.commit()
            return True
        except Exception, err:
            return err
        finally:
            conn.close()

    def update_param(self, diction, table_names, condition=""):
        args = []
        if not isinstance(table_names, basestring):
            table_names = ", ".join(table_names)

        for key in diction:
                args.append(diction[key])

        if isinstance(diction, dict):
            diction = ", ".join(" {}=? ".format(key) for key in diction)

        conn = sqlite3.connect(self.dbfile)
        conn.text_factory = str

        try:
            cursor = conn.execute("update {0} set {1} {2}".format(table_names, diction, condition), args)
            conn.commit()
            return cursor.lastrowid
        except Exception, err:
            return err
        finally:
            conn.close()

    def delete(self, table_names, condition=""):

        conn = sqlite3.connect(self.dbfile)
        conn.text_factory = str

        try:
            cursor = conn.execute("delete from {0} where {1}".format(table_names, condition))
            conn.commit()
            return True
        except Exception, err:
            return err
        finally:
            conn.close()
