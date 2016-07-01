from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from ..models import LogEntry
# from ..util import paginate


class EventLogView(TemplateView):
    template_name = 'students/events_log.html'

    def get_context_data(self, **kwargs):
        context = super(EventLogView, self).get_context_data(**kwargs)
        context['events_log_url'] = reverse('events_log')

        events_log = LogEntry.objects.all()
        # .order_by('timestamp').reverse()[:100]

        # events_log = [
        #     {'timestamp': '2016.01.01-15:01', 'evt_type': 'C', 'evt_user': 'User1', 'evt_description': 'Created user Ivanov A.A.'},
        #     {'timestamp': '2016.01.01-16:01', 'evt_type': 'U', 'evt_user': 'User1', 'evt_description': 'Updated user Ivanov A.A.'},
        #     {'timestamp': '2016.01.01-17:01', 'evt_type': 'D', 'evt_user': 'User123', 'evt_description': 'Deleted user Petrenko P.P.'},
        #     {'timestamp': '2016.01.01-18:01', 'evt_type': 'U', 'evt_user': 'User123', 'evt_description': 'Updated user Salo S.S.'},
        # ]

        context['events_log'] = events_log

        # apply pagination, 2 groups per page
        # context.update(paginate(events_log, 2, self.request, {}, var_name='events_log'))

        return context
