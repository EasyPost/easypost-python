# imports
import os
import platform
import sys
import urllib
import urlparse
import time
import datetime
import types
import re

from version import VERSION
import importer
json = importer.import_json()

# cStringIO is faster - use where available!
try:
  import cStringIO as StringIO
except ImportError:
  import StringIO

# use urlfetch as request_lib on google app engine, otherwise use requests
request_lib = None
try:
  from google.appengine.api import urlfetch
  request_lib = 'urlfetch'
except ImportError:
  try:
    import requests
    request_lib = 'requests'
  except ImportError:
    raise ImportError('EasyPost requires an up to date requests library. Update requests via "pip install -U requests" or contact us at contact@easypost.co.')

  try:
    version = requests.__version__
    major, minor, patch = [int(i) for i in version.split('.')]
  except Exception:
    raise ImportError('EasyPost requires an up to date requests library. Update requests via "pip install -U requests" or contact us at contact@easypost.co.')
  else:
    if major < 1:
      raise ImportError('EasyPost requires an up to date requests library. Update requests via "pip install -U requests" or contact us at contact@easypost.co.')

# config
api_key = None
#api_base = 'https://www.geteasypost.com/api/v2'
#api_base = 'https://easyposttest.herokuapp.com/api/v2'
api_base = 'http://localhost:5000/api/v2'

# exceptions
class EasyPostError(Exception):
  def __init__(self, message=None, http_status=None, http_body=None, json_body=None):
    super(EasyPostError, self).__init__(message)
    self.http_status = http_status
    self.http_body = http_body
    self.json_body = json_body

class AuthenticationError(EasyPostError):
  pass

class APIError(EasyPostError):
  pass

class NetworkError(EasyPostError):
  pass

class InvalidRequestError(EasyPostError):
  def __init__(self, message, param, http_status=None, http_body=None, json_body=None):
    super(InvalidRequestError, self).__init__(message, http_body, http_status, json_body)
    self.param = param

def convert_to_easypost_object(response, api_key):
  types = { 'Address' : Address,
            'ScanForm' : ScanForm,
            'CustomsItem' : CustomsItem,
            'CustomsInfo' : CustomsInfo,
            'Parcel' : Parcel,
            'Shipment': Shipment,
            'Rate' : Rate,
            'PostageLabel': PostageLabel }

  if isinstance(response, list):
    return [convert_to_easypost_object(i, api_key) for i in response]
  elif isinstance(response, dict):
    response = response.copy()
    cls_name = response.get('object', EasyPostObject)
    if isinstance(cls_name, basestring):
      cls = types.get(cls_name, EasyPostObject)
    else:
      cls = EasyPostObject
    return cls.construct_from(response, api_key)
  else:
    return response

class Requestor(object):
  def __init__(self, local_api_key=None):
    self.api_key = local_api_key

  @classmethod
  def api_url(cls, url=''):
    return '%s%s' % (api_base, url)

  @classmethod
  def _utf8(cls, value):
    if isinstance(value, unicode):
      return value.encode('utf-8')
    else:
      return value

  @classmethod
  def encode_dict(cls, out, key, dict_value):
    n = {}
    for k, v in dict_value.iteritems():
      k = cls._utf8(k)
      v = cls._utf8(v)
      n["%s[%s]" % (key, k)] = v
    out.extend(cls._encode_inner(n))

  @classmethod
  def encode_list(cls, out, key, list_value):
    for v in list_value:
      v = cls._utf8(v)
      out.append(("%s[]" % (key), v))

  @classmethod
  def encode_datetime(cls, out, key, dt_value):
    utc_timestamp = int(time.mktime(dt_value.timetuple()))
    out.append((key, utc_timestamp))

  @classmethod
  def encode_none(cls, out, key):
    pass # do not include None-valued params in request

  @classmethod
  def _encode_inner(cls, params):
    # special case value encoding
    ENCODERS = {
      list: cls.encode_list,
      dict: cls.encode_dict,
      datetime.datetime: cls.encode_datetime,
      types.NoneType: cls.encode_none,
    }

    out = []
    for key, value in params.iteritems():
      key = cls._utf8(key)
      try:
          encoder = ENCODERS[value.__class__]
          encoder(out, key, value)
      except KeyError:
        # don't need special encoding
        value = unicode(value)
        out.append((key, value))
    return out

  @classmethod
  def _objects_to_ids(cls, param):
    if isinstance(param, Resource):
      return {'id': param.id}
    elif isinstance(param, dict):
      out = {}
      for k, v in param.iteritems():
        out[k] = cls._objects_to_ids(v)
      return out
    else:
      return param

  @classmethod
  def encode(cls, params):
    return urllib.urlencode(cls._encode_inner(params))

  @classmethod
  def build_url(cls, url, params):
    base_query = urlparse.urlparse(url).query
    if base_query:
      return '%s&%s' % (url, cls.encode(params))
    else:
      return '%s?%s' % (url, cls.encode(params))

  def request(self, method, url, params={}):
    http_body, http_status, my_api_key = self.request_raw(method, url, params)
    response = self.interpret_response(http_body, http_status)
    return response, my_api_key

  def request_raw(self, method, url, params={}):
    my_api_key = self.api_key or api_key

    if my_api_key is None:
      raise AuthenticationError('No API key provided. Set your API key via "easypost.api_key = \'APIKEY\'"). Please contact us at contact@easypost.co if you do not know where to find your API key.')

    abs_url = self.api_url(url)
    params = params.copy()
    self._objects_to_ids(params)

    ua = {
      'client_version' : VERSION,
      'lang' : 'python',
      'publisher' : 'easypost',
      'request_lib': request_lib,
      }
    for attr, func in [['lang_version', platform.python_version],
                       ['platform', platform.platform],
                       ['uname', lambda: ' '.join(platform.uname())]]:
      try:
        val = func()
      except Exception, e:
        val = "!! %s" % e
      ua[attr] = val

    headers = {
      'X-EasyPost-Client-User-Agent' : json.dumps(ua),
      'User-Agent' : 'EasyPost/v2 PythonClient/%s' % (VERSION, ),
      'Authorization' : 'Bearer %s' % (my_api_key, )
      }
    
    print abs_url
    print params
    print "*"*20

    if request_lib == 'urlfetch':
      http_body, http_status = self.urlfetch_request(method, abs_url, headers, params)
    elif request_lib == 'requests':
      http_body, http_status = self.requests_request(method, abs_url, headers, params)
    else:
      raise EasyPostError("Bug discovered: invalid request_lib: %s. Please report to contact@easypost.co" % (request_lib))

    return http_body, http_status, my_api_key

  def interpret_response(self, http_body, http_status):
    try:
      response = json.loads(http_body)
    except Exception:
      raise APIError("Invalid response body from API: (%d) %s " % (http_body, http_status), http_body, http_status)
    if not (200 <= http_status < 300):
      self.handle_api_error(http_body, http_status, response)
    return response

  def requests_request(self, method, abs_url, headers, params):
    method = method.lower()
    if method == 'get' or method == 'delete':
      if params:
        abs_url = self.build_url(abs_url, params)
      data = None
    elif method == 'post':
      data = self.encode(params)
    else:
      raise NetworkError("Bug discovered: invalid request method: %s. Please report to contact@easypost.co" % (method))

    try:
      result = requests.request(method, abs_url, headers=headers, data=data, timeout=60, verify=False)
      http_body = result.content
      http_status = result.status_code
    except Exception as e:
      print e
      raise NetworkError("Unexpected error communicating with EasyPost.  If this problem persists, let us know at contact@easypost.co.")
    return http_body, http_status

  def urlfetch_request(self, method, abs_url, headers, params):
    args = {}
    if method == 'post':
      args['payload'] = self.encode(params)
    elif method == 'get' or method == 'delete':
      abs_url = self.build_url(abs_url, params)
    else:
      raise NetworkError("Bug discovered: invalid request method: %s. Please report to contact@easypost.co" % (method))

    args['url'] = abs_url
    args['method'] = method
    args['headers'] = headers
    args['validate_certificate'] = False
    args['deadline'] = 55 # GAE times out after 60

    try:
      result = urlfetch.fetch(**args)
    except:
      raise NetworkError("Unexpected error communicating with EasyPost.  If this problem persists, let us know at contact@easypost.co.")

    return result.content, result.status_code

  def handle_api_error(self, http_body, http_status, response):
    try:
      error = response['error']
    except (KeyError, TypeError):
      raise APIError("Invalid response from API: %r (HTTP status code was %d)" % (http_body, http_status), http_body, http_status, response)

    if http_status in [400, 404]:
      raise InvalidRequestError(error.get('message'), error.get('param'), http_body, http_status, response)
    elif rcode == 401:
      raise AuthenticationError(error.get('message'), http_body, http_status, response)
    else:
      raise APIError(error.get('message'), http_body, http_status, response)


class EasyPostObject(object):
  def __init__(self, id=None, api_key=None, **params):
    self.__dict__['_values'] = set()
    self.__dict__['_unsaved_values'] = set()
    self.__dict__['_transient_values'] = set()
    self.__dict__['_immutable_values'] = set(['api_key', 'id'])
    self.__dict__['_retrieve_params'] = params

    self.__dict__['api_key'] = api_key

    if id:
      self.id = id

  def __setattr__(self, k, v):
    self.__dict__[k] = v
    self._values.add(k)
    if k not in self._immutable_values:
      self._unsaved_values.add(k)

  def __getattr__(self, k):
    try:
      return self.__dict__[k]
    except KeyError:
      pass
    raise AttributeError("%r object has no attribute %r" % (type(self).__name__, k))

  def __getitem__(self, k):
    if k in self._values:
      return self.__dict__[k]
    else:
      raise KeyError(k)

  def get(self, k, default=None):
    try:
      return self[k]
    except KeyError:
      return default

  def setdefault(self, k, default=None):
    try:
      return self[k]
    except KeyError:
      self[k] = default
      return default

  def __setitem__(self, k, v):
    setattr(self, k, v)

  def keys(self):
    return self._values.keys()

  def values(self):
    return self._values.keys()

  @classmethod
  def construct_from(cls, values, api_key):
    instance = cls(values.get('id'), api_key)
    instance.refresh_from(values, api_key)
    return instance

  def refresh_from(self, values, api_key, partial=False):
    self.api_key = api_key

    if partial:
      removed = set()
    else:
      removed = self._values - set(values)

    for k in removed:
      if k in self._immutable_values:
        continue
      del self.__dict__[k]
      self._values.discard(k)
      self._transient_values.add(k)
      self._unsaved_values.discard(k)

    for k, v in values.iteritems():
      if k in self._immutable_values:
        continue
      self.__dict__[k] = convert_to_easypost_object(v, api_key)
      self._values.add(k)
      self._transient_values.discard(k)
      self._unsaved_values.discard(k)

  def __repr__(self):
    type_string = ''
    if isinstance(self.get('object'), basestring):
      type_string = ' %s' % self.get('object').encode('utf8')

    id_string = ''
    if isinstance(self.get('id'), basestring):
      id_string = ' id=%s' % self.get('id').encode('utf8')

    return '<%s%s%s at %s> JSON: %s' % (type(self).__name__, type_string, id_string, hex(id(self)), json.dumps(self.to_dict(), sort_keys=True, indent=2, cls=EasyPostObjectEncoder))

  def __str__(self):
    return json.dumps(self.to_dict(), sort_keys=True, indent=2, cls=EasyPostObjectEncoder)

  def to_dict(self):
    def _serialize(o):
      if isinstance(o, EasyPostObject):
        return o.to_dict()
      if isinstance(o, list):
        return [_serialize(i) for i in o]
      return o

    d = dict()
    for k in sorted(self._values):
      v = getattr(self, k)
      v = _serialize(v)
      d[k] = v
    return d

class EasyPostObjectEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, EasyPostObject):
      return obj.to_dict()
    else:
      return json.JSONEncoder.default(self, obj)

class Resource(EasyPostObject):
  def _ident(self):
    return [self.get('id')]

  @classmethod
  def retrieve(cls, id, api_key=None, **params):
    instance = cls(id, api_key, **params)
    instance.refresh()
    return instance

  def refresh(self):
    requestor = Requestor(self.api_key)
    url = self.instance_url()
    response, api_key = requestor.request('get', url, self._retrieve_params)
    self.refresh_from(response, api_key)
    return self

  @classmethod
  def class_name(cls):
    if cls == Resource:
      raise NotImplementedError('Resource is an abstract class. You should perform actions on its subclasses.')

    cls_name = cls.__name__
    cls_name = cls_name[0:1] + re.sub('([A-Z])', '_\1', cls_name[1:])
    return "%s" % cls_name.lower()

  @classmethod
  def class_url(cls):
    cls_name = cls.class_name()
    if cls_name[-1:] == "s":
      return "/%ses" % cls_name
    else:
      return "/%ss" % cls_name

  def instance_url(self):
    id = self.get('id')
    if not id:
      raise InvalidRequestError('%s instance has invalid ID: %r' % (type(self).__name__, id), 'id')
    id = Requestor._utf8(id)
    base = self.class_url()
    param = urllib.quote_plus(id)
    return "%s/%s" % (base, param)

# API resource classes
class AllResource(Resource):
  @classmethod
  def all(cls, api_key=None, **params):
    requestor = Requestor(api_key)
    url = cls.class_url()
    response, api_key = requestor.request('get', url, params)
    return convert_to_easypost_object(response, api_key)

class CreateResource(Resource):
  @classmethod
  def create(cls, api_key=None, **params):
    requestor = Requestor(api_key)
    url = cls.class_url()
    response, api_key = requestor.request('post', url, params)
    return convert_to_easypost_object(response, api_key)

class UpdateResource(Resource):
  def save(self):
    if self._unsaved_values:
      requestor = Requestor(self.api_key)
      params = {}
      for k in self._unsaved_values:
        params[k] = getattr(self, k)
      url = self.instance_url()
      response, api_key = requestor.request('post', url, params)
      self.refresh_from(response, api_key)

    return self

class DeleteResource(Resource):
  def delete(self, **params):
    requestor = Requestor(self.api_key)
    url = self.instance_url()
    response, api_key = requestor.request('delete', url, params)
    self.refresh_from(response, api_key)
    return self

# API resource objects
class Address(AllResource, CreateResource):
  pass

class ScanForm(AllResource, CreateResource):
  pass

class CustomsItem(AllResource, CreateResource):
  pass

class CustomsInfo(AllResource, CreateResource):
  pass

class Parcel(AllResource, CreateResource):
  pass

class Shipment(AllResource, CreateResource):
  pass

class Rate(AllResource, CreateResource):
  pass

class PostageLabel(AllResource, CreateResource):
  pass
