from wrapper import Wrapper
from conf import Conf
from apps.models.sys_const import SysConst
import os

class TemlateLetter(object):

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_FOLDER = os.path.join(APP_ROOT, '../../templates')
    LETTER_FILE = os.path.join(TEMPLATE_FOLDER, 'template_letter.html')

    def __init__(self):
        self.w = Wrapper()

    def get_template_letter(self, tittle="", hello="", message="",from_site="",site="",mail=""):
        try:
            data=""
            with open(self.LETTER_FILE, 'r') as myfiletemplate:
                data=myfiletemplate.read().replace('\n', '')
            data=data.replace('[TITLE]',tittle).replace('[HELLO]',hello).replace('[MESSAGE]',message).replace('[FROM]',from_site).replace('[SITE]',site).replace('[MAIL]',mail)
            ###print data
            return data
        except Exception, e:
            print e
            return ""
        

