# -*- coding: utf-8 -*-
import mail

if __name__ == '__main__':
    mailer = mail.PHPMailer('http://example.com/script.php')
    mailer.attachments.append('send_mail.php')
    print mailer.send_mail('tz4678@gmail.com', u'Тест', u'Это тестовое сообщение.')