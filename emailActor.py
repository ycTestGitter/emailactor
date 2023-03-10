#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        emailActor.py
#
# Purpose:     This module is used to read and write email.
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2022/12/28
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

# Gmail configure:
# Turn on the Less secure app access at: Google Account> Security> Less secure app access
# Enable the IMAP Access at: Gmail Settings> Forwarding and POP / IMAP> IMAP Acess

import time
import smtplib
import imaplib
import email
import traceback 

SMTP_PORT = 993

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class emailActor(object):
    """ GMail: smtpPort[993], sslConn[True]
        HotMail: smtpPort[587], sslConn[True]
        Mailu: smtpPort[143], sslConn[True]

    Args:
        object (_type_): _description_
    """

    def __init__(self, account, password, smtpServer, smtpPort=SMTP_PORT, sslConn=True) -> None:
        self.account = account
        self.password = password
        self.mailHandler = None
        try:
            self.mailHandler = imaplib.IMAP4_SSL(host=smtpServer, port=smtpPort) if sslConn else imaplib.IMAP4(host=smtpServer, port=smtpPort)
            self.mailHandler.login(self.account, self.password)
        except Exception as err:
            print("Login the email server failed.")
            print("Error: %s" %str(err))
            return None

#-----------------------------------------------------------------------------
    def readLastMail(self, sender=None, emailNum=10, interval=0):
        try:
            self.mailHandler.select('inbox')
            emailInfo = self.mailHandler.search(None, 'ALL') if sender is None else self.mailHandler.search(None, 'FROM', f'"{sender}"')
            IdList = emailInfo[1][0].split() 
            
            mailIds = IdList if len(IdList) < emailNum else IdList[-emailNum:]
            print(mailIds)
            for mailId in mailIds:
                msg = self._getEmailDict(mailId)
                if msg:
                    print(msg.keys())
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
                    #print('Body : ' + str(msg) + '\n')
                    if interval> 0 : time.sleep(interval)
                print("--Finish")
        except Exception as e:
            traceback.print_exc() 
            print(str(e))

#-----------------------------------------------------------------------------
    def _getEmailDict(self, emailId):
        """ Get the email info.
        Args:
            emailIdx (_type_): _description_
        """
        mailId = int(emailId)
        data = self.mailHandler.fetch(str(mailId), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                try:
                    return email.message_from_string(str(arr[1],'utf-8'))
                except:
                    return None


def testCase(mode):
    account = 'alice@gt.org'
    account = 'bob@gt.org'
    account = 'charles@gt.org'
    password = '123'
    smtpServer = 'email.gt.org'
    smtpPort = 143
    actor = emailActor(account, password, smtpServer, smtpPort=smtpPort, sslConn=False)
    actor.readLastMail(emailNum=2)

if __name__ == '__main__':
    testCase(1)