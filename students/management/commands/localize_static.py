from django.core.management.base import BaseCommand
from optparse import make_option
import requests
from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from django.conf import settings


class Command(BaseCommand):
    args = '<--online|--offline>'
    help = 'Set localize static to online/offline usage'
    option_list = BaseCommand.option_list + (
        make_option('-n', '--online', action="store_false", dest="ls", help='Set localize static to online'),
        make_option('-f', '--offline', action="store_true", dest="ls", help='Set localize static to offline')
    )

    app = 'students'
    app_static_path = app + settings.STATIC_URL
    html_template = 'students/base.html'
    html_file = app + '/templates/' + html_template

    def handle(self, *args, **options):
        if settings.DEBUG:
            if options['ls'] is None:
                self._get_status()
            else:
                self._set_offline() if options['ls'] else self._set_online()
        else:
            self.stdout.write('Command "Localize_static" for debug mode only!')
        return

    def _set_offline(self):
        # search online urls in rendered template
        urls = self._get_online_urls()
        if not urls:
            self.stdout.write('No online urls. Localized static status: offline')
            return
        # read template to raw string
        t = self._read_html_file()
        # TODO: create comment map list
        comment_map = [(1, 15), (20, 30)]
        for (url, static_type) in urls:
            # download from CDN to static
            if not self._save_CDN_files(url, static_type):
                return
            # search url in template
            url_idx_start, search = 0, True
            while search:
                url_idx = t.find(url, url_idx_start, len(t))
                if url_idx:
                    search = False
                    # exclude if url found in comment tags
                    for (comment_open_idx, comment_close_idx) in comment_map:
                        if (comment_open_idx < url_idx) and (url_idx+len(url) < comment_close_idx):
                            url_idx_start, search = comment_close_idx, True
                else:
                    self.stdout.write('Error! Found in urls, but not found in templates!')
                    self.stdout.write('%s' % url)
                    self.stdout.write('Is url split by "\" in template? Concatenate it, please.')
                    return
            # search <link*> or <script*>*</script> tag indexes for this url
            (tag_open, tag_close) = ('<', '>' if static_type is 'css' else '</script>')
            tag_open_idx = t.rfind(tag_open, 0, url_idx)
            tag_close_idx = t.find(tag_close, url_idx + len(url), len(t))
            if tag_open_idx and tag_close_idx:
                # prepare to replace online tag by offline tag
                tag_online = t[tag_open_idx:tag_close_idx+len(tag_close)]
                tag_online_comment = '<!--' + tag_online[:] + '-->'
                static_file = static_type + '/' + self._get_file_name(url)
                static_url = '{{ PORTAL_URL }}{% static "' + static_file + '" %}'
                tag_offline = tag_online_comment + '\n' + tag_online[:].replace(url, static_url)
                # replace tag
                t = t.replace(tag_online, tag_offline)
            else:
                self.stdout.write('Error! Broken HTML in templates!')
                return
        # save raw string to template
        self._save_html_file(t)
        return

    def _set_online(self):
        urls = self._get_offline_urls()
        if not urls:
            self.stdout.write('No offline urls. Localized static status: online')
            return
        # html_comment_tag = ('<!--', '-->')
        # django_comment_tag = ('{#', '#}')
        # link_tag = ('<link', '>')
        # script_tag = ('<script', '</script>')
        return

    def _get_status(self):
        s = 'online' if self._get_online_urls() else 'offline'
        self.stdout.write('Localized static status: %s' % s)
        return

    def _save_CDN_files(self, url, static_type):
        self.stdout.write('Download from %s...' % url)
        try:
            static_path = self.app_static_path + static_type + '/' + self._get_file_name(url)
            response = requests.get(url, stream=True, timeout=10)
            with open(static_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        except Exception as e:
            self.stdout.write('Error! %s' % e.message)
            return False
        else:
            self.stdout.write('OK')
        return True

    def _get_file_name(self, url):
        return url.split('/')[-1].split('?')[0]

    def _read_html_file(self):
        with open(self.html_file, 'r') as f:
            return f.read()

    def _save_html_file(self, t):
        with open(self.html_file, 'w') as f:
            f.write(t)
        return

    def _get_offline_urls(self):
        t = self._read_html_file()
        urls = []
        return urls

    def _get_online_urls(self):
        soup = BeautifulSoup(render_to_string(self.html_template, {}))
        urls = [(tag['href'], 'css') for tag in soup.select('link[href*="//"]')]
        urls += [(tag['src'], 'js') for tag in soup.select('script[src*="//"]')]
        # urls += [(tag['src'], 'img') for tag in soup.select('img[src*="//"]')]
        return urls
