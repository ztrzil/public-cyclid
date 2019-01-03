#!/usr/bin/env python
import imaplib
import smtplib
import uuid


def main():
    try:
        user = 'utkvolsec@gmail.com'
        password = 'VRxWKjWV9ixtB3WEq8aYz3B3uDPzg'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        send_to = 'utkvolsec@gmail.com'
        server.starttls()
        server.login(user, password)
        id = uuid.uuid4()
        msg = "{}".format(str(id));
        server.sendmail(user, send_to, msg)
        server.quit()

        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        mail.login(user, password)
        mail.list()
        mail.select("inbox")
        result, data = mail.search(None, "ALL")

        ids = data[0]
        for mail_id in ids.split():
            result, data = mail.fetch(mail_id, "(RFC822)")  # fetch the email body (RFC822) for the given ID
            if str(id) in str(data[0][1]):
                return True
        return False

    except Exception:
        return False


if __name__ == '__main__':
    main()
