from io import BytesIO
from lxml import etree
import requests


class ClientError:

    def __init__(self, code=None, message=None, tracking_id=None):
        self.code = code
        self.message = message
        self.tracking_id = tracking_id


class ClientException(Exception):

    def __init__(self, response=None, content=None):
        self.content = content
        self.errors = None
        self.response = response
        if isinstance(content, dict):
            self._init_json()
        else:
            self._init_xml()

    def error(self):
        return None if self.errors is None else self.errors[0]

    def _init_json(self):
        try:
            self.errors = list(map(self._json_error,
                                   self.content['errorList']['error']))
        except (KeyError, TypeError):
            self.errors = None

    def _init_xml(self):
        self.errors = list(map(self._xml_error,
                               self.content.xpath('/errorList/error')))

    def _json_error(self, e):
        return ClientError(code=e['errorCode'], message=e['errorMessage'],
                           tracking_id=e['trackingId'])

    def _xml_error(self, e):
        return ClientError(code=e.xpath('errorCode').text,
                           message=e.xpath('errorMessage').text,
                           tracking_id=e.xpath('trackingId').text)


class Client:

    URL = 'https://api-{region}.hosted.exlibrisgroup.com/almaws/v{ver}/{url}'

    def __init__(self, api_key=None, lang='en', region='eu', timeout=None,
                 version='1'):
        if api_key is None or api_key == '':
            raise ValueError('api_key is required')
        self.api_key = api_key
        self.lang = lang
        self.region = region
        self.timeout = timeout
        self.version = version

    def call(self, endpoint, method='GET', params=None, data=None, headers=None):
        try:
            res = requests.request(method.upper(), self.url(endpoint),
                                   params=self._params(params),
                                   data=data,
                                   headers=self._headers(headers))
            return self._response(res)
        except requests.exceptions.RequestException as e:
            raise ClientException from e

    def url(self, endpoint=None, region=None, version=None):
        if region is None:
            region = self.region
        if version is None:
            version = self.version
        return self.URL.format(region=region, ver=version, url=endpoint)

    def _headers(self, init_headers=None):
        result = {
            'Accept': 'application/json;q=0.9,application/xml;q=0.8',
            'Authorization': 'apikey {api_key}'.format(api_key=self.api_key),
        }
        if init_headers:
            result.update(init_headers)
        return result

    def _params(self, init_params=None):
        result = {
            'lang': self.lang
        }
        if init_params:
            result.update(init_params)
        return result

    @classmethod
    def _response(cls, res):
        content = cls._response_content(res)
        if res.status_code == requests.codes.ok:
            return content
        raise ClientException(content=content, response=res)

    @classmethod
    def _response_content(cls, res):
        content_type, rest = res.headers['content-type'].split(';')
        if content_type == 'application/json':
            return res.json()
        elif content_type == 'application/xml':
            return etree.parse(BytesIO(res.content))
        else:
            return res.text
