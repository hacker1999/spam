# -*- coding: utf-8 -*-
import base64
import urllib
import json

# адрес скрипта обработчика
handler_url = ''

def base64_encode(s):
    return base64.b64encode(s.encode('utf-8'))

def encode_value(s):
    if type(s) is unicode:
        return '=?UTF-8?B?%s?=' % base64_encode(s)
    return s

def chunk_split(s, length = 76, end = '\r\n', **kwargs):
    si = 0
    L = []
    while si < len(s):
        ei = si + length
        chunk = s[si:ei]
        L.append(chunk)
        si = ei
    return '\r\n'.join(L)

def send_mail(to, subject = '', message, header = {}, **kwargs):
    header['Content-Type'] = 'text/html; charset=utf-8'
    header['Content-Transfer-Encoding'] = 'base64'
    header = header.items()
    for i in range(len(header)):
        pair = header[i]
        header[i] = '%s: %s' % (pair[0], encode_value(pair[1]))
    header = '\r\n'.join(header)
    payload = {
        'to': to,
        'subject': encode_value(subject),
        'message': chunk_split(base64_encode(message)),
        'header': header,
        'send': 1
    }
    res = urllib.urlopen(handler_url, urllib.urlencode(payload))
    data = res.read().decode('utf-8')
    return json.loads(data)