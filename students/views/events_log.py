from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from ..models import LogEntry
from ..util import paginate


class EventLogView(TemplateView):
    template_name = 'students/events_log.html'

    def get_context_data(self, **kwargs):
        context = super(EventLogView, self).get_context_data(**kwargs)
        context['events_log_url'] = reverse('events_log')

        events_log = LogEntry.objects.all().order_by('-timestamp')
        context['events_log'] = events_log

        # apply pagination, 10 events per page
        context.update(paginate(events_log, 10, self.request, {}, var_name='events_log'))

        return context
