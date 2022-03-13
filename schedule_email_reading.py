from email_utility      import read_email
# from ner_utility        import perform_ner
from database_utility   import insert_emails, get_num_read_emails, set_num_read_emails

import imaplib
import time
import os
import pandas as pd


#Fetching mailEx account credentials
username = os.environ.get("MAILEX_EMAIL_ID")
password = os.environ.get("MAILEX_EMAIL_PASSWORD")


if __name__ == '__main__':
    while True:

        #Creating an IMAP4 class with SSL 
        imap = imaplib.IMAP4_SSL("imap.gmail.com")

        #Authenticating with credentials
        imap.login(username, password)

        #Selecting the 'INBOX' labels
        status, messages = imap.select("INBOX")

        #Total number of emails
        num_total_emails = int(messages[0])

        #Number of emails that have been read
        num_read_emails = get_num_read_emails()#int(open('num_read_emails.txt', 'r').read())

        #Dataframe for storing new emails read
        emails = pd.DataFrame()

        print(f'Emails Read: {num_read_emails}, Total Emails: {num_total_emails}')


        ###------READ EMAILS-----####
        for i in range(num_total_emails, num_read_emails, -1):

            emails = emails.append(read_email(imap, i), ignore_index=True)
        #####-------------------#####


        #Saving number of emails read
        # open('num_read_emails.txt', 'w').write(str(num_total_emails))
        set_num_read_emails(num_total_emails)

        #Closing the connection and logging out
        imap.close()
        imap.logout()

        #Performing NER on emails
        # emails = perform_ner(emails)

        #Perfroming RE on emails
        ###-----HERE-----###

        #Updating Database by adding new emails
        # insert_emails(emails)

        for email in emails.iterrows():
            print(email)
            print('-'*50)
                

        #Emptying the emails dataframe
        del emails

        #Sleeping for 'x' amount of time
        print('Sleeping for 60s')
        print('##'*30)
        time.sleep(60)
                    

        


