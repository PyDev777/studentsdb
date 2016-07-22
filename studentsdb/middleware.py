from datetime import datetime
from django.http import HttpResponse
from bs4 import BeautifulSoup
from settings import DEBUG
# import time


class RequestTimeMiddleware(object):
    """Display request time on a page"""

    def process_request(self, request):
        if DEBUG:
            request.start_time = datetime.now()
        return None

    def process_view(self, request, view, args, kwargs):
        return None

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return HttpResponse('Exception found: %s' % exception)

    def process_response(self, request, response):
        if DEBUG and hasattr(request, 'start_time') and ('text/html' in response.get('Content-Type', '')):
            soup = BeautifulSoup(response.content, 'lxml')
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
