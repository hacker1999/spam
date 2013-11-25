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
        chunk = s[si:ei]
        L.append(chunk)
        si = ei
    return end.join(L)

class PHPMailer(object):
    def __init__(self, script_url, charset = 'UTF-8', user_agent = '', **kwargs):
        self.script_url = script_url
        self.charset = charset
        self.user_agent = user_agent
        self.attachments = []

    def stob64(self, s):
        return base64.b64encode(s.encode(self.charset))

    def mime_encode(self, s):
        if type(s) is unicode:
            return '=?%s?B?%s?=' % (self.charset, self.stob64(s))
        return s

    def send_mail(self, to_addr, subject, message, is_html = 0, headers = {}, **kwargs):
        message_type = 'text/%s; charset=%s' % ('html' if is_html else 'plain', self.charset)
        message_encoded = chunk_split(self.stob64(message))
        if len(self.attachments):
            boundary = '--Boundary_' + uuid.uuid4().hex
            headers['Content-Type'] = 'multipart/mixed; boundary="%s"' % boundary
            sys_encoding = sys.getfilesystemencoding()
            L = []
            # сообщение
            L.extend([
                '--' + boundary,
                'Content-Type: ' + message_type,
                'Content-Transfer-Encoding: base64',
                '',
                message_encoded
            ])
            # аттачи
            for filename in self.attachments: 
                extension = os.path.splitext(filename)[1]
                content_type = mimetypes.types_map[extension] if extension in mimetypes.types_map else 'application/octet-stream'
                basename = os.path.basename(filename).encode(sys_encoding)
                L.extend([
                    '--' + boundary,
                    'Content-Type: %s; name="%s"' % (content_type, basename),
                    'Content-Disposition: attachment',
                    'Content-Transfer-Encoding: base64',
                    '',
                    chunk_split(base64.b64encode(open(filename.encode(sys_encoding), 'rb').read()))
                ])
            L.extend([
                '--' + boundary + '--',
                ''
            ])
            mail_body = '\r\n'.join(L)
        else:
            headers['Content-Type'] = message_type
            headers['Content-Transfer-Encoding'] = 'base64'
            mail_body = message_encoded
        headers = headers.items()
        for i in range(len(headers)):
            pair = headers[i]
            headers[i] = '%s: %s' % (pair[0], self.mime_encode(pair[1]))
        headers = '\r\n'.join(headers)
        payload = {
            'to_addr': to_addr,
            'subject': self.mime_encode(subject),
            'body': mail_body,
            'additional_headers': headers,
            'send_mail': 1
        }
        req = urllib2.Request(self.script_url,
                              urllib.urlencode(payload),
                              {
                                'User-Agent': self.user_agent
                              })
        res = urllib2.urlopen(req)
        data = res.read()
        parts = res.info()['content-type'].split(';')
        if len(parts) > 1:
            pair = parts[1].trim().split('=')
            if (pair[0].lower() == 'charset'):
                data = data.decode(pair[1])
        return json.loads(data)