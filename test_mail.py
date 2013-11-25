# -*- coding: utf-8 -*-
import mailbomber

if __name__ == '__main__':
    mailer = mailbomber.MailBomber('http://example.com/send_mail.php')
    mailer.add_header('Reply-to', 'tz4678@gmail.com')
    mailer.attach(u'Текстовый документ.txt')
    print mailer.send_mail('anonimnyy13@bk.ru', u'Тест', u'Это тестовое сообщение.')
