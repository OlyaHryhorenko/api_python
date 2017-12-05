from wrapper import Wrapper
from conf import Conf
from apps.models.sys_const import SysConst
import os

class CreateSiteMap(object):

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_FOLDER = os.path.join(APP_ROOT, '../../static')
    SITEMAP_FILE = os.path.join(TEMPLATE_FOLDER, 'sitemap.xml')

    def __init__(self):
        self.w = Wrapper()

    def create_sitemap(self):
        begin_root_node='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'
        end_root_node="</urlset>"
        try:
            alldatalink=SysConst().GetAll_Sys_Sitemap()
            site_name=str(SysConst().Get_Sys_Const("site_name")[:-1]).lower()
            if (alldatalink):
                with open(self.SITEMAP_FILE, 'w') as sitemap_file:
                    sitemap_file.write('{0}\n'.format(begin_root_node))
                    for rec in alldatalink:
                        print rec
                        sitemap_file.write('<url>\n')
                        sitemap_file.write('<loc>\n')
                        sitemap_file.write('{0}{1}\n'.format(site_name,str(rec["sysfield"]).replace("/index.html","/")))
                        sitemap_file.write('</loc>\n')
                        sitemap_file.write('<changefreq>')
                        sitemap_file.write('{}'.format(rec["changefreq"]))
                        sitemap_file.write('</changefreq>\n')
                        sitemap_file.write('<priority>')
                        sitemap_file.write('{}'.format(rec["priority"]))
                        sitemap_file.write('</priority>\n')
                        sitemap_file.write('</url>\n')
                    sitemap_file.write('{0}\n'.format(end_root_node))
            return True
        except Exception, e:
            print e
            return False