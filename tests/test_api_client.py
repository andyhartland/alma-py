from lxml import etree
from ..api.client import Client, ClientException
from .test_helper import Test


class ClientTest(Test):

    URL = 'https://api-{region}.hosted.exlibrisgroup.com/almaws/v{ver}/{url}'

    def setUp(self):
        super(ClientTest, self).setUp()
        self.client = Client(api_key=self.api_key, lang=self.lang,
                             region=self.region, version=self.version)
        pass

    def test_call_general_config(self):
        endpoint = 'conf/general'
        result = self.client.call(endpoint)
        # Expect a dict (parsed JSON)
        self.assertIsInstance(result, dict)
        # Expect the correct Alma institution code and name
        alma_inst = result.get('institution', None)
        self.assertEqual(alma_inst['desc'], self.alma_inst['desc'])
        self.assertEqual(alma_inst['value'], self.alma_inst['value'])
        pass

    def test_call_report(self):
        # Expect an XML document
        self.call_report()

    def test_call_report_exception(self):
        with self.assertRaises(ClientException):
            self.call_report(limit=1)

    def test_client_defaults(self):
        client = Client(self.api_key)
        self.assert_client_properties(client)

    def test_client_properties(self):
        self.assert_client_properties(self.client, api_key=self.api_key,
                                      lang=self.lang, region=self.region,
                                      version=self.version)

    def test_client_url(self):
        region = 'na'
        version = '2'
        endpoint = 'analystics/reports'
        exp_url = self.url(endpoint, region=region, version=version)
        actual_url = self.client.url(endpoint, region=region, version=version)
        self.assertEqual(exp_url, actual_url)

    def test_client_url_default(self):
        endpoint = 'analytics/reports'
        exp_url = self.url(endpoint)
        actual_url = self.client.url(endpoint)
        self.assertEqual(exp_url, actual_url)

    def test_client_without_api_key(self):
        with self.assertRaises(ValueError):
            Client()
        with self.assertRaises(ValueError):
            Client('')

    def assert_client_exception(self, exception, expected=None):
        # Get the actual error codes from the exception
        error_codes = map(lambda e: e.code, exception.errors)
        if expected is None:
            expected = []
        # Assert that all expected error codes are present
        for exp in expected:
            self.assertIn(error_codes, exp)

    def assert_client_properties(self, client, api_key=None, lang='en',
                                 region='eu', version='1'):
        if api_key is None:
            api_key = self.api_key
        self.assertEqual(api_key, client.api_key)
        self.assertEqual(lang, client.lang)
        self.assertEqual(region, client.region)
        self.assertEqual(version, client.version)

    def call_report(self, limit=25, path=None):
        endpoint = 'analytics/reports'
        if path is None:
            path = self.report
        headers = {'Accept': 'application/xml;q=1.0'}
        params = {'path': path, 'limit': limit}
        return self.client.call(endpoint, params=params, headers=headers)

    def url(self, endpoint=None, region='eu', version='1'):
        return self.URL.format(region=region, ver=version, url=endpoint)
