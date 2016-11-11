# coding: utf-8

from django.core.management.base import BaseCommand
from optparse import make_option
from django.template.loader import render_to_string as rts, TemplateDoesNotExist
from bs4 import BeautifulSoup as bs, Comment
import requests
from django.conf import settings


class Command(BaseCommand):
    args = '<--online|--offline>'
    help = 'Set static to online/offline usage in base.html template.'
    option_list = BaseCommand.option_list + (
        make_option('-n', '--online', action="store_false", dest="ls", help='Set localize static to online'),
        make_option('-f', '--offline', action="store_true", dest="ls", help='Set localize static to offline')
    )
    app, html_template = 'students', 'students/base.html'
    app_static_path, html_file = app + settings.STATIC_URL, app + '/templates/' + html_template

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self._err_exit('Command "Localize_static" for debug mode only!')
        if options['ls'] is None:
            self.stdout.write('Localized static status: %s' % ('online' if self._get_CDN_tags() else 'offline'))
        else:
            self._set_offline() if options['ls'] else self._set_online()

    def _set_offline(self):
        tags = self._get_CDN_tags()
        if not tags:
            self.stdout.write('No CDN tags.\nLocalized static status: offline')
            return
        t = self._read_html_file()
        for tag in tags:
            self._save_CDN_file(tag)
            ref_idx = t.find(tag['ref'])
            if ref_idx < 0:
                self._err_exit('Ref %s not found (split by "\\"?) in template file!' % tag['ref'])
            open_idx = t.rfind(tag['open'], 0, ref_idx)
            if open_idx < 0:
                self._err_exit('Open tag for %s not found!' % tag['ref'])
            close_idx = t.find(tag['close'][0], ref_idx + len(tag['ref']))
            if close_idx < 0:
                self._err_exit('Close tag for %s not found!' % tag['ref'])
            online_str = t[open_idx:close_idx + 1]
            offline_str = online_str.replace(tag['ref'], tag['static_ref'])
            t = t.replace(online_str, '<!--' + online_str + tag['close'][1] + '-->\n' + offline_str)
        self._save_html_file(t)
        self.stdout.write('Localized static status: offline')

    def _set_online(self):
        tags = self._get_commented_CDN_tags()
        if not tags:
            self.stdout.write('No commented CDN tags.\nLocalized static status: online')
            return
        t = self._read_html_file()
        for tag in tags:
            c = tag['comment'].output_ready()
            c_idx = t.find(c)
            if c_idx < 0:
                self._err_exit('Commented tag %s not found (split by "\\"?) in template file!' % c)
            s_open_idx = t.find(tag['open'], c_idx + len(c))
            if s_open_idx > 0:
                s_close_idx = t.find(tag['close'][0], s_open_idx + len(tag['open']))
                if s_close_idx < 0:
                    self._err_exit('Static close tag for %s not found!' % tag['ref'])
                if tag['static_path'] in t[s_open_idx:s_close_idx]:
                    online_str = tag['comment'].replace(tag['close'][1], '')
                    t = t.replace(t[c_idx:s_close_idx + 1], online_str)
        self._save_html_file(t)
        self.stdout.write('Localized static status: online')

    def _save_CDN_file(self, tag):
        self.stdout.write('Download file: %s ...' % tag['ref'])
        r = requests.get(tag['ref'], stream=True, timeout=5)
        if r.status_code != 200:
            self._err_exit('Response status code: %s' % r.status_code)
        try:
            with open(self.app_static_path + tag['static_path'], 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        except Exception as e:
            self._err_exit(e.message)
        self.stdout.write('OK')

    def _get_CDN_tags(self):
        return self._unitags(bs(self._get_template()).select('link[href*="//"], script[src*="//"]'))

    def _get_commented_CDN_tags(self):
        def get_comment(s):
            return s if isinstance(s, Comment) and '//' in s and s.strip()[:4] in ['<lin', '<scr'] else ''
        comments = bs(self._get_template()).find_all(string=get_comment)
        tags = self._unitags(bs(str(comments)).select('link[href*="//"], script[src*="//"]'))
        if tags:
            for tag in tags:
                for comment in comments:
                    if tag['open'] in comment and tag['ref'] in comment:
                        tag['comment'] = comment
        return tags

    def _unitags(self, tags):
        for tag in tags:
            js = tag.name == 'script'
            ref = 'src' if js else 'href'
            tag['ref_type'] = ref
            tag['ref'] = tag[ref]
            tag['open'] = '<script ' if js else '<link '
            tag['close'] = ('>', '</script>') if js else ('>', '')
            tag['static_path'] = ('js/' if js else 'css/') + tag[ref].split('/')[-1].split('?')[0]
            tag['static_ref'] = '{{ PORTAL_URL }}{% static ' + '\"' + tag['static_path'] + '\"' + ' %}'
            tag['comment'] = 'No comment.'
        return tags

    def _get_template(self):
        try:
            t = rts(self.html_template, {})
        except TemplateDoesNotExist as e:
            self._err_exit(e.message)
        else:
            return t

    def _read_html_file(self):
        try:
            with open(self.html_file, 'r') as f:
                t = f.read()
        except IOError as e:
            self._err_exit('Template file %s: %s!' % (self.html_file, e.strerror))
        else:
            return t

    def _save_html_file(self, t):
        try:
            with open(self.html_file, 'w') as f:
                f.write(t)
        except IOError as e:
            self._err_exit('Template file %s: %s!' % (self.html_file, e.strerror))

    def _err_exit(self, msg):
        self.stdout.write('ERROR!\n%s\nBase template not modified.' % msg)
        raise SystemExit(1)
