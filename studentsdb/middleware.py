from datetime import datetime
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.conf import settings
from django.db import connection
# import time


class DBTimeMiddleware(object):
    """Display DB time on a page"""

    def __init__(self):
        self.db_time = 0
        self.db_qcount = 0

    def process_exception(self, request, exception):
        return HttpResponse('Exception found: %s' % exception)

    def process_response(self, request, response):
        if settings.DEBUG:
            self.db_qcount = len(connection.queries)
            self.db_time += sum([float(q['time']) for q in connection.queries])
            if 'text/html' in response.get('Content-Type', ''):
                soup = BeautifulSoup(response.content)
                if soup.body:
                    tag = soup.new_tag('code', style='position: fixed; top: 0; left: 0px')
                    tag.string = 'DB took: %s, DB queries count: %s' % (str(self.db_time), str(self.db_qcount))
                    soup.body.insert(0, tag)
                    response.content = soup.prettify()
        return response


class RequestTimeMiddleware(object):
    """Display request time on a page"""

    def process_request(self, request):
        if settings.DEBUG:
            request.start_time = datetime.now()
        return None

    def process_view(self, request, view, args, kwargs):
        return None

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return HttpResponse('Exception found: %s' % exception)

    def process_response(self, request, response):
        if settings.DEBUG and hasattr(request, 'start_time') and ('text/html' in response.get('Content-Type', '')):
            soup = BeautifulSoup(response.content)
            if soup.body:
                # time.sleep(2)
                dtime = datetime.now() - request.start_time
                if dtime.seconds < 2:
                    tag = soup.new_tag('code', style='position: fixed; top: 0; right: 0')
                    tag.string = 'Request took: %s' % str(dtime)
                    soup.body.insert(0, tag)
                    response.content = soup.prettify()
                else:
                    response = HttpResponse('<h2>Processing of request too slow. Developer - check your code!<h2>')
        return response
