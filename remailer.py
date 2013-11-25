# -*- coding: utf-8 -*-
import base64
import uuid
import sys
import os
import mimetypes
import urllib
import urllib2
import json

def chunk_split(s, length = 76, end = '\r\n', **kwargs):
    si = 0
    L = []
    while si < len(s):
        ei = si + length
        L.append(s[si:ei])
        si = ei
    return end.join(L)

def stob64(s, charset):
    return base64.b64encode(s.encode(charset))

def mime_encode(s, charset):
    return '=?%s?B?%s?=' % (charset, stob64(s, charset))

class ReMailer(object):
    def __init__(self, script_url, charset = 'UTF-8', client_headers = {}, **kwargs):
        self.script_url = script_url
        self.charset = charset
        self.client_headers = client_headers
        self.mail_headers = {}
        self.attachments = []

    def add_header(self, name, value):
        self.mail_headers[name] = value

    def attach(self, *args):
        """instance.attach('file'[, 'file1'[, ...]])"""
        self.attachments += args

    def stob64(self, s):
        return base64.b64encode(s.encode(self.charset))

    def send_mail(self, to_addr, subject, message, is_html = 0):
        message_content_type = 'text/%s; charset=%s' % ('html' if is_html\
                                                               else 'plain', self.charset)
        message_encoded = chunk_split(stob64(message, self.charset))
        headers = dict(self.mail_headers)
        if len(self.attachments):
            boundary = '--Boundary_' + uuid.uuid4().hex
            headers['Content-Type'] = 'multipart/mixed; boundary=%s' % boundary
            sys_encoding = sys.getfilesystemencoding()
            L = []
            L.extend([
                '--' + boundary,
                'Content-Type: ' + message_content_type,
                'Content-Transfer-Encoding: base64',
                '',
                message_encoded
            ])
            for f in self.attachments: 
                extension = os.path.splitext(f)[1]
                content_type = mimetypes.types_map[extension] if extension in mimetypes.types_map\
                                                              else 'application/octet-stream'
                name = mime_encode(os.path.basename(f), sys_encoding)
                content = open(f.encode(sys_encoding), 'rb').read()
                L.extend([
                    '--' + boundary,
                    'Content-Type: %s; name="%s"' % (content_type, name),
                    'Content-Disposition: attachment; filename="%s"' % name,
                    'Content-Transfer-Encoding: base64',
                    '',
                    chunk_split(base64.b64encode(content))
                ])
            L.extend([
                '--' + boundary + '--',
                ''
            ])
            body = '\r\n'.join(L)
        else:
            headers['Content-Type'] = message_content_type
            headers['Content-Transfer-Encoding'] = 'base64'
            body = message_encoded
        headers = headers.items()
        for i in range(len(headers)):
            pair = headers[i]
            headers[i] = '%s: %s' % (pair[0], pair[1])
        headers = '\r\n'.join(headers)
        payload = {
            'to_addr': to_addr,
            'subject': mime_encode(subject, self.charset),
            'body': body,
            'headers': headers,
            'send_mail': 1
        }
        req = urllib2.Request(self.script_url,
                              urllib.urlencode(payload),
                              self.client_headers)
        res = urllib2.urlopen(req)
        data = res.read()
        # http://www.w3.org/Protocols/rfc1341/4_Content-Type.html
        parts = res.info()['content-type'].split(';')
        if len(parts) > 1:
            i = 1
            params = {}
            while i < len(parts):
                pair = parts[i].split('=', 1)
                if len(pair) == 2:
                    params[pair[0].strip().lower()] = pair[1].strip()
                i += 1
            if 'charset' in params:
                # print params['charset']
                data = data.decode(params['charset'])
        # print data
        return json.loads(data)
