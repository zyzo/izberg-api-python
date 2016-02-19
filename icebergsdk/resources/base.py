# -*- coding: utf-8 -*-
import warnings, sys, json, logging, time
import weakref  # Means that if there is no other value, it will be removed
import pytz
from datetime import datetime, date
from dateutil import parser as date_parser
from decimal import Decimal
logger = logging.getLogger('icebergsdk.resource')

from icebergsdk.exceptions import IcebergNoHandlerError, IcebergReadOnlyError,\
    IcebergMultipleObjectsReturned, IcebergObjectNotFound


"""
Work in progress...
Lot's of stuff to rewrite/remove/add
"""
class IcebergJSONEncoder(json.JSONEncoder):
    """ 
    Iceberg Encoder handling special types
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return obj.to_eng_string()
        else:
            return super(IcebergJSONEncoder, self).default(obj)


class IcebergObject(dict):
    __objects_store = {} # Will store the object for relationship management
    raw_fields = []
    DATETIME_FIELDS = []
    GENERIC_DATETIME_FIELDS = [
        "timestamp", "last_modified", "creation_date", 
        "created_on", "last_updated", "last_update", "last_sync", "updated_at", "created_at"
    ]

    DECIMAL_FIELDS = []
    GENERIC_DECIMAL_FIELDS = [
        "price", "price_with_vat", "price_without_vat",
        "previous_price", "previous_price_with_vat", "previous_price_without_vat",
        "original_price", "original_price_with_vat", "original_price_without_vat",
    ]

    def __init__(self, api_key=None, handler = None, **params):
        super(IcebergObject, self).__init__()

        self._unsaved_values = set()
        self._transient_values = set()

        self._retrieve_params = params
        self._previous_metadata = None

        object.__setattr__(self, '_handler', handler)

    def __setattr__(self, k, v):
        if k[0] == '_':
            return super(IcebergObject, self).__setattr__(k, v)

        if k in self.__dict__:
            self._init_unsaved()
            self._unsaved_values.add(k)

            return super(IcebergObject, self).__setattr__(k, v)
        else:
            self._init_unsaved()
            self._unsaved_values.add(k)
            self[k] = v

    def __nonzero__(self):
        return True

    def _init_unsaved(self):
        # Allows for unpickling in Python 3.x
        if not hasattr(self, '_unsaved_values'):
            self._unsaved_values = set()

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __setitem__(self, k, v):
        if v == "":
            raise ValueError(
                "You cannot set %s to an empty string. "
                "We interpret empty strings as None in requests."
                "You may set %s.%s = None to delete the property" % (
                    k, str(self), k))

        super(IcebergObject, self).__setitem__(k, v)

        # Allows for unpickling in Python 3.x
        if not hasattr(self, '_unsaved_values'):
            self._unsaved_values = set()

        self._unsaved_values.add(k)

    def __getitem__(self, k):
        try:
            return super(IcebergObject, self).__getitem__(k)
        except KeyError as err:
            if k in self._transient_values:
                raise KeyError(
                    "%r.  HINT: The %r attribute was set in the past."
                    "It was then wiped when refreshing the object with "
                    "the result returned by Stripe's API, probably as a "
                    "result of a save().  The attributes currently "
                    "available on this object are: %s" %
                    (k, k, ', '.join(self.keys())))
            else:
                raise err

    def __delitem__(self, k):
        raise TypeError(
            "You cannot delete attributes on a IcebergObject. "
            "To unset a property, set it to None.")

    def request(self, *args, **kwargs):
        return self._handler.request(*args, **kwargs)

    def get_list(self, resource, **kwargs):
        """
        Return a list of Resource Objects
        """
        data = self._handler.get_list(resource, **kwargs)

        res = []
        for element in data:
            res.append(IcebergObject.findOrCreate(self._handler, element))

        return res

    def send_image(self, *args, **kwargs):
        return self._handler.send_image(*args, **kwargs)

    def to_JSON(self):
        return json.dumps(self.as_dict(), cls=IcebergJSONEncoder)

    def as_dict(self, max_depth=4):
        params = {}
        if max_depth <= 0:
            return self.resource_uri if hasattr(self, "resource_uri") else {}
        for k in self.__dict__:
            if k.startswith('_'):
                continue

            v = getattr(self, k)

            if isinstance(v, IcebergObject):
                params[k] = v.as_dict(max_depth=max_depth-1)
            elif type(v) == list:
                res = []
                for u in v:
                    if isinstance(u, IcebergObject):
                        res.append(u.as_dict(max_depth=max_depth-1))
                    elif hasattr(u, 'as_dict'):
                        res.append(u.as_dict())
                    else:
                        res.append(u)
                params[k] = res
            else:
                params[k] = v # if v is not None else ""
        return params

    def __repr__(self):        
        ident_parts = [type(self).__name__]

        if isinstance(self.get('object'), basestring):
            ident_parts.append(self.get('object'))

        if isinstance(self.get('id'), basestring):
            ident_parts.append('id=%s' % (self.get('id'),))

        unicode_repr = '<%s at %s> JSON: %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

        if sys.version_info[0] < 3:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

    def __str__(self):
        # return json.dumps(self, sort_keys=True, indent=2) ## was always {}
        return json.dumps(
            self.as_dict(max_depth=1), 
            sort_keys=True, indent=2, 
            cls=IcebergJSONEncoder
        )


    def to_dict(self):
        warnings.warn(
            'The `to_dict` method is deprecated and will be removed in '
            'version 2.0 of the Stripe bindings. The StripeObject is '
            'itself now a subclass of `dict`.',
            DeprecationWarning)

        return dict(self)

    def iceberg_id(self):
        return self.id

    def is_new(self):
        return getattr(self, 'id', None) is None

    def has_changed(self):
        return len(self._unsaved_values) > 0

    @classmethod
    def build_resource_uri(cls, options):
        """
        Generate a resource URI from a class

        Should work like:
            build_resource_uri(Product, {id:2}) -> https://api.iceberg.technology/v1/product/2/
        """
        raise NotImplementedError()

    def get_resource_uri(self):
        if self.is_new():
            raise Exception('Missing id for resource %s' % self.endpoint)

        if not hasattr(self, 'resource_uri'):
            self.resource_uri = "/v1/%s/%s/" % (self.endpoint, self.id)
        return self.resource_uri

    def _load_attributes_from_response(self, **response):
        """
        Loads attributes
        If the data has a nested object with a resource_uri, try to math an existing object
        """
        for key, value in response.iteritems():
            if key == "meta":
                continue
            if type(value) == list:
                res = []
                for elem in value:
                    if type(elem)==dict and 'resource_uri' in elem: # Try to match a relation
                        try:
                            from icebergsdk.resources import get_class_from_resource_uri
                            obj_cls = get_class_from_resource_uri(elem['resource_uri'])
                            res.append(obj_cls.findOrCreate(self._handler, elem))
                        except Exception:
                            logger.exception('Cant parse resource')
                    else:
                        res.append(elem)
                        
                self.__dict__[key] = res

            elif type(value) == dict:
                if len(value) == 0:
                    self.__dict__[key] = None
                elif key in self.raw_fields:
                    self.__dict__[key] = value ## keep this field as raw
                elif 'resource_uri' in value: # Try to match a relation
                    try:
                        from icebergsdk.resources import get_class_from_resource_uri
                        obj_cls = get_class_from_resource_uri(value['resource_uri'])
                        self.__dict__[key] = obj_cls.findOrCreate(self._handler, value)
                    except:
                        ## keep it as dict
                        self.__dict__[key] = value
                elif 'id' in value: # Fall back
                    self.__dict__[key] = value['id']
                else:
                    self.__dict__[key] = value ## keep it as dict
            elif value and key in (self.DATETIME_FIELDS + self.GENERIC_DATETIME_FIELDS):
                if type(value) == int:
                    self.__dict__[key] = datetime.fromtimestamp(value, tz=pytz.utc)
                else:
                    self.__dict__[key] = date_parser.parse(value)
            elif value and key in (self.DECIMAL_FIELDS + self.GENERIC_DECIMAL_FIELDS):
                self.__dict__[key] = Decimal(str(value))
            else:
                self.__dict__[key] = value
        return self


    @classmethod
    def findOrCreate(cls, handler, data):
        """
        Take a dict and return an corresponding Iceberg resource object.

        Check in _objects_store for reuse of existing object

        Example:
            data: {
                "id": 1,
                "resource_uri": "/v1/user/1/"
                ...
            }

            Will return an User object
        """

        from icebergsdk.resources import get_class_from_resource_uri

        try:
            obj_cls = get_class_from_resource_uri(data['resource_uri'])
        except:
            obj = cls(handler=handler)
        else:
            data_type = obj_cls.endpoint

            if "pk" in data:
                key = str(data['pk'])
            else:
                key = str(data['id'])

            if not data_type in handler._objects_store: # New type collectore
                handler._objects_store[data_type] = weakref.WeakValueDictionary()
                obj = obj_cls(handler=handler)
                handler._objects_store[data_type][key] = obj
            else:
                if key in handler._objects_store[data_type]:
                    obj = handler._objects_store[data_type][key]
                else:
                    obj = obj_cls(handler=handler)
                    handler._objects_store[data_type][key] = obj


        return obj._load_attributes_from_response(**data)


    @classmethod
    def find(cls, handler, object_id):
        if not handler:
            raise IcebergNoHandlerError()
        data = handler.get_element(cls.endpoint, object_id)
        return cls.findOrCreate(handler, data)


    @classmethod
    def search(cls, handler, args = None):
        if not handler:
            raise IcebergNoHandlerError()

        data = handler.request("%s/" % cls.endpoint, args)
        res = []
        for element in data['objects']:
            res.append(cls.findOrCreate(handler, element))

        return res, data["meta"]  # cls.findOrCreate(data)


    @classmethod
    def findWhere(cls, handler, args):
        """
        Like search but return the first result
        """
        results, meta = cls.search(handler, args)
        if len(results) > 1:
            raise IcebergMultipleObjectsReturned()
        elif len(results) == 0:
            raise IcebergObjectNotFound()
        return results[0]


    @classmethod
    def all(cls, handler, args = None):
        """
        Like search but return the first result
        """
        return cls.search(handler, args)[0]


    def validate_format(self):
        """
        Check the data with the format structure sent by the API
        """
        raise NotImplementedError()


    def fetch(self, return_meta=False):
        """
        Resets the model's state from the server
        """
        if not self._handler:
            raise IcebergNoHandlerError()

        data = self._handler.request(self.resource_uri)
        meta = data.pop('meta', {})

        self._load_attributes_from_response(**data)
        
        if return_meta:
            return self, meta
        else:
            return self


    def delete(self):
        raise IcebergReadOnlyError()


    def save(self):
        raise IcebergReadOnlyError()


    def wait_for_value(self, value_name, expected_value, max_wait=60, retry_every=5):
        """ 
        Returns True if 'value_name' equals 'expected_value' before 'max_wait' seconds else False
        """
        self.fetch()
        timeout = time.time() + max_wait
        while time.time() < timeout  and not getattr(self, value_name) == expected_value:
            logger.debug("Waiting %s seconds for value '%s' to change to '%s'" %
                (retry_every, value_name, expected_value)
            )
            time.sleep(retry_every)
            self.fetch()

        if getattr(self, value_name) == expected_value:
            return True
        else:
            logger.warn(
                u"Waited %s seconds, value '%s' is still '%s' (!=%s)" % 
                (max_wait, value_name, getattr(self, value_name), expected_value)
            )
            return False


def dict_force_text(anything):
    if isinstance(anything, str): ## ex: anything = 'étoile' in a coding: utf-8 file
        return anything.decode("utf-8").encode("utf-8")
    elif isinstance(anything, unicode): ## ex: anything = u'étoile'
        return anything.encode("utf-8")
    elif isinstance(anything, Decimal):
        return str(anything)
    elif isinstance(anything, dict):
        new_dict = {}
        for key, value in anything.iteritems():
            new_dict[dict_force_text(key)] = dict_force_text(value)
        return new_dict
    elif isinstance(anything, list):
        return [dict_force_text(item) for item in anything]
    else: 
        return anything

class UpdateableIcebergObject(IcebergObject):

    def serialize(self, obj):
        params = {}
        if obj._unsaved_values:
            for k in obj._unsaved_values:
                if k == 'id' or k == '_previous_metadata':
                    continue
                v = getattr(obj, k)

                if isinstance(v, IcebergObject):
                    params[k] = v.get_resource_uri()
                elif type(v) == list:

                    res = []
                    for elem in v:
                        if isinstance(elem, IcebergObject):
                            res.append(elem.get_resource_uri())
                        else:
                            res.append(elem)
                    params[k] = res
                else:
                    params[k] = v # if v is not None else ""
        
        params = dict_force_text(params)
        
        return params


    def save(self, handler = None):
        if not handler:
            if not self._handler:
                raise IcebergNoHandlerError()

            handler = self._handler

        if self.is_new():
            method = "POST"
            path = "%s/" % self.endpoint
        else:
            method = "PUT"
            path = self.resource_uri

        res = handler.request(path, post_args = self.serialize(self), method = method)
        self._load_attributes_from_response(**res)

        # Clean
        self._unsaved_values = set()

        return self


    def delete(self, handler = None):
        if not handler:
            if not self._handler:
                raise IcebergNoHandlerError()

            handler = self._handler
                
        handler.request(self.resource_uri, post_args = {}, method = "DELETE")
        # Clean
        self.__dict__ = {}
        self._unsaved_values = set()


