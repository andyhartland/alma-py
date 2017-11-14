import os
import dotenv
import unittest


dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
dotenv.load_dotenv(dotenv_path)


class Test(unittest.TestCase):
    def setUp(self):
        self.alma_inst = {
            'desc': os.environ.get('ALMA_INST_NAME'),
            'value': os.environ.get('ALMA_INST_CODE')
        }
        self.alma_inst_name = os.environ.get('ALMA_INST_NAME')
        self.api_key = os.environ.get('ALMA_API_KEY')
        self.lang = os.environ.get('ALMA_API_LANG')
        self.region = os.environ.get('ALMA_API_REGION')
        self.report = os.environ.get('ALMA_REPORT')
        self.version = os.environ.get('ALMA_API_VERSION')
