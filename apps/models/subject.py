import re


class Subject(object):
    table_sub_grp = "SubjectGroups"
    table_sbj_st = "SubjectStatuses"
    table_subject = "Subjects"

    def __init__(self, wrapper):
        if wrapper is None:
            raise TypeError

        self.w = wrapper

    def get_list_active_subj(self):
        """

        :return: list active subject for orders form
        """
        try:
            return self.w.select(" SQL_CACHE sbj.id, sbj.subject, sbj_gr.group ",
                                 self.table_subject,
                                 (" as sbj " +
                                  " join " +
                                  " {0} as sbj_st " +
                                  " on sbj.id_status=sbj_st.id " +
                                  " join " +
                                  " {1} as sbj_gr " +
                                  " on sbj.id_group=sbj_gr.id " +
                                  " where sbj.id_status={2} " +
                                  " Order by sbj_gr.group, sbj.subject ").format(self.table_sbj_st,
                                                                                 self.table_sub_grp,
                                                                                 1)
                                 )
        except Exception, e:
            print e
        finally:
            pass

    def add_subject(self, sbj):
        """
        Add ubject to table - Subjects
        :param sbj: list fields
        :return: id insert record
        """
        return self.w.insert(sbj, self.table_subject)

    def upd_subject(self, sbj, condition=""):
        """
        Update record in table - Subjects
        :param sbj: list fields
        :param condition: condtition in WHERE
        :return: status query
        """
        return self.w.update(sbj, self.table_subject, condition)
