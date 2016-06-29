from local_settings import PORTAL_PROTOCOL, PORTAL_DOMAIN, PORTAL_PORT


def students_proc(request):
    return {'PORTAL_URL': PORTAL_PROTOCOL + '://' + PORTAL_DOMAIN + ':' + PORTAL_PORT}

# def students_proc(request):
#     return {'PORTAL_URL': request.scheme + '://' + request.get_host()}
