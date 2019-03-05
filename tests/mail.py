#!/usr/bin/env python
import imaplib
import smtplib
import uuid


def main():
    # send an email with a unique ID (to ourselves)
    user = 'nobody@erebus.eecs.utk.edu'
    server = smtplib.SMTP('erebus.eecs.utk.edu', 25)
    send_to = user
    id = uuid.uuid4()
    msg = "{}".format(str(id));
    server.sendmail(user, send_to, msg)
    server.quit()

    return True


if __name__ == '__main__':
    main()
