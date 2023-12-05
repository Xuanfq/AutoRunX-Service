

def is_method_GET(request):
    return request.method == 'GET'


def is_method_POST(request):
    return request.method == 'POST'


def is_method_PUT(request):
    return request.method == 'PUT'


def is_method_DELETE(request):
    return request.method == 'DELETE'


def is_method_CONNECT(request):
    return request.method == 'CONNECT'


def is_method_OPTIONS(request):
    return request.method == 'OPTIONS'


def is_method_HEAD(request):
    return request.method == 'HEAD'


def is_method_TRACE(request):
    return request.method == 'TRACE'


def datetime2jsobject(datetime):
    if datetime is None:
        return None
    return int(datetime.timestamp()*1000)
