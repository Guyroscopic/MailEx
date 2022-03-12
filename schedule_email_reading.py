from email_utility import read_email

import imaplib
import time
import os
import flair
import pandas as pd


def perform_ner(sentence):

    entities = [ span.to_dict() for span in sentence.get_spans() ]
    for entity in entities:
        entity['labels'] = entity['labels'][0].to_dict()

    return entities


#Fetching mailEx account credentials
username = os.environ.get("MAILEX_EMAIL_ID")
password = os.environ.get("MAILEX_EMAIL_PASSWORD")

NERtagger = flair.models.SequenceTagger.load('flair/ner-english-ontonotes-large')

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
        num_read_emails = 8#int(open('email_utils/num_read_emails.txt', 'r').read())

        #Dataframe for storing new emails read
        emails = pd.DataFrame()

        # print(f'Emails Read: {num_read_emails}, Total Emails: {num_total_emails}')


        ###------READ EMAILS-----####
        for i in range(num_total_emails, num_read_emails, -1):

            emails = emails.append(read_email(imap, i), ignore_index=True)
        #####-------------------#####


        #Saving number of emails read
        # open('num_read_emails.txt', 'w').write(str(num_total_emails))

        #Closing the connection and logging out
        imap.close()
        imap.logout()

        ###------PROCESS EMAILS AND SAVE TO DATABASE-----####
        emails['sentences'] = emails['cleaned_body'].apply(flair.data.Sentence)
        # sentences = [
        #     flair.data.Sentence(email['Cleaned'])
        #     for email in emails
        # ]

        NERtagger.predict(emails['sentences'].to_list())

        emails['entities'] = emails['sentences'].apply(perform_ner)
           
        out = emails.to_json(orient= 'records', default_handler= str, indent= 4)
        
        open('out.json', 'w').write(out)

        # predictions = [[ 
        #     span.to_dict() 
            
        #     for span     in sentence.get_spans()
        # ]   for sentence in sentences
        # ] 

        for email in emails.iterrows():
            print(email)
            print('-'*50)
                
        # print(predictions[0])
        # print(type(predictions[0]))
        # print(predictions[0])
        #####-------------------------------------------#####

        #Emptying the emails List
        del emails

        #Sleeping for 'x' amount of time
        print('Sleeping for 60s')
        print('##'*30)
        time.sleep(60)
                    

        


