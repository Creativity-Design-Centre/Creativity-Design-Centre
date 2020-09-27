from urllib.parse import urlparse, urlencode

_url = input('')
_parse = urlparse(_url)
_query = _parse.query
_query_spilt = _query.split('&')

_hasPageNum = False
_new_params = {}

for i in _query_spilt:
    key = i.split('=')[0]
    value = i.split('=')[1]
    if key == 'pageNumber':
        _hasPageNum = True
        if not value == 1:
            value = int(value) + 1
    _new_params[key] = value


if not _hasPageNum:
    _new_params['pageNumber'] = 1
    # print(_query_spilt)

_new_url = _parse.scheme + '://' + _parse.netloc + \
    _parse.path + '?' + urlencode(_new_params)

print(_new_url)
