from wrapper import Wrapper


class Api(object):

    def __init__(self, wrapper):
        if wrapper is None:
            raise TypeError

        self.w = wrapper
        self.NAME = 'ApiSitesData'

    def get_all(self):
        return self.w.select("SQL_CACHE *", self.NAME)

    def get_data_by_id(self, site_id):
        return self.w.select(["*"], self.NAME, "where site_id=%s" % site_id)
