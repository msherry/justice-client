from datetime import datetime
import json

import iso8601
import wac


__version__ = '0.1'

__all__ = [
]


# client


_TYPE_TO_ERROR = {}


def _convert_error(ex):
    if not hasattr(ex.response, 'data') or 'type' not in ex.response.data:
        return ex
    message = wac.Error.format_message(ex)
    exc = _TYPE_TO_ERROR.get(ex.response.data['type'], Error)
    return exc(message, **ex.response.data)


class _ErrorMeta(type):

    def __new__(meta_cls, name, bases, dict):
        cls = type.__new__(meta_cls, name, bases, dict)
        cls.TYPES = [
            getattr(cls, k)
            for k in dir(cls)
            if k.isupper() and isinstance(getattr(cls, k), basestring)
        ]
        _TYPE_TO_ERROR.update(zip(cls.TYPES, [cls] * len(cls.TYPES)))
        return cls


class Error(Exception):

    __metaclass__ = _ErrorMeta

    def __init__(self, *args, **kwargs):
        super(Error, self).__init__(*args)
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __repr__(self):
        attrs = ', '.join([
            '{}={}'.format(k, repr(v))
            for k, v in self.__dict__.iteritems()
        ])
        return '{}({}, {})'.format(
            self.__class__.__name__,
            ' '.join(self.args),
            attrs)


def configure(root_url, **kwargs):
    default = kwargs.pop('default', True)
    kwargs['client_agent'] = 'justice-client/' + __version__
    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    kwargs['headers']['Accept-Type'] = 'application/json'
    kwargs['error_class'] = kwargs.get('error_class', _convert_error)
    if default:
        default_config.reset(root_url, **kwargs)
    else:
        Client.config = wac.Config(root_url, **kwargs)


default_config = wac.Config(None, error_class=_convert_error)


class Client(wac.Client):

    config = default_config

    @staticmethod
    def _default_serialize(o):
        if isinstance(o, datetime):
            return o.isoformat() + 'Z'
        raise TypeError(
            'Object of type {} with value of {} is not JSON serializable'
            .format(type(o), repr(o)))

    def _serialize(self, data):
        data = json.dumps(data, default=self._default_serialize)
        return 'application/json', data

    def _deserialize(self, response):
        if response.headers['Content-Type'] != 'application/json':
            raise Exception("Unsupported content-type '{}'"
                            .format(response.headers['Content-Type']))
        data = json.loads(response.content)
        return self._parse_deserialized(data)

    @staticmethod
    def _parse_deserialized(e):
        if isinstance(e, dict):
            for key in e.iterkeys():
                if key.endswith('_at') and isinstance(e[key], basestring):
                    e[key] = iso8601.parse_date(e[key])
        return e


# resources

class Resource(wac.Resource):

    client = Client()
    registry = wac.ResourceRegistry()


def health():
    return Resource.client.get('/health').content
