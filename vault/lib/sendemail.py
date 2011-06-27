# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

from __future__ import division, with_statement, print_function

# Import smtplib for the actual sending function
from smtplib import SMTP, SMTP_SSL, SMTPAuthenticationError, SMTPRecipientsRefused

# Import the email modules we'll need
from email.mime.text import MIMEText

from lib.config import Config

#    Do last!
from lib.logger import Logger
log = Logger('library')


def sendemail(subject, message_text):
    config = Config.get_config()
    if not (config.mail_server and config.mail_port and config.mail_to and config.mail_from):
        raise Exception("Mail has not been configured")
    sendemail2(config.mail_server, config.mail_port, config.mail_ssl, config.mail_from, config.mail_to,
               config.mail_auth, config.mail_login, config.mail_password, subject, message_text)

def sendemail2(server, port, ssl, from_addr, to_addr, auth, login, password, subject, message_text):
    try:
        if not server or not port or not from_addr or not to_addr:
            raise Exception(_("Mail has not been configured"))
        if not subject or not message_text:
            raise Exception(_("Subject and message text cannot be empty"))
        log.trace("send_mail starting", server, port, ssl, from_addr, to_addr, auth, login, password, subject, message_text)
        msg = MIMEText(message_text)
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = ", ".join(to_addr.split(";"))

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        if ssl:
            log.debug("SMTP SSL")
            s = SMTP_SSL(server, int(port), timeout=20)
        else:
            log.debug("SMTP")
            s = SMTP(server, int(port), timeout=20)
        try:
            s.set_debuglevel(False)
            if auth:
                log.debug("Attempting to authenticate")
                s.login(login, password)
                log.debug("Completed")
            log.debug("Sending")
            fail_users = s.sendmail(from_addr, to_addr.split(";"), msg.as_string())
            if len(fail_users) > 0:
                raise Exception("Some recipients were rejected (%s)" % (",".join(fail_users.keys())))
            log.debug("Done Send")
        finally:
            s.quit()
        return True
    except SMTPAuthenticationError as e:
        raise Exception(_("Login/Password are incorrect"))
    except SMTPRecipientsRefused as e:
        raise Exception(_("All recipients were rejected."))
    except Exception as e:
        raise Exception(_("Mail send failed. %s") % str(e))

    log.trace("send_email completed")
