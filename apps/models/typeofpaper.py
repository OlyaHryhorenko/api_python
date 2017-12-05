import re


class OrderAssignment(object):
    table_assign_st = "OrderAssignmentStatuses"
    table_assign = "OrderAssignment"

    def __init__(self, wrapper):
        if wrapper is None:
            raise TypeError

        self.w = wrapper

    def get_list_active_orderassign(self):
        """

        :return: list active subject for orders form
        """
        try:
            return self.w.select(" SQL_CACHE assign.id, assign.prefix, assign.assignment ",
                                 self.table_assign,
                                 (" as assign " +
                                  " join " +
                                  " {0} as assign_st " +
                                  " on assign.id_status=assign_st.id " +
                                  " where assign.id_status={1} " +
                                  " Order by assign.assignment ").format(self.table_assign_st, 1)
                                 )
        except Exception, e:
            print e
        finally:
            pass

    def get_asign_prefix(self, assign_id=''):
        """
        Return assign prefix for uid work
        :param assign_id: id record
        :return: prefix
        """
        try:
            return self.w.select(" assign.prefix ",
                                 self.table_assign,
                                 (" as assign " +
                                  " where assign.id={0} " +
                                  " ").format(assign_id)
                                 )
        except Exception, e:
            print e
        finally:
            pass

    def add_subject(self, sbj):
        """
        Add ubject to table - OrderAssignment
        :param sbj: list fields
        :return: id insert record
        """
        return self.w.insert(sbj, self.table_assign)

    def upd_subject(self, sbj, condition=""):
        """
        Update record in table - OrderAssignment
        :param sbj: list fields
        :param condition: condtition in WHERE
        :return: status query
        """
        return self.w.update(sbj, self.table_assign, condition)
