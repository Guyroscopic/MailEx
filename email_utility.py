from email.header import decode_header

import email, unicodedata, re


def remove_URL(text):
    """
    Remove URLs from a sample string
    """

    return re.sub(r"http\S+", "", text)

def remove_non_ascii(words):
    """
    Remove non-ASCII characters from list of tokenized words
    """

    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return ' '.join(new_words)


def clean_text(text):

    cleaned_text = remove_URL(text)
    cleaned_text = remove_non_ascii(cleaned_text.split())

    return cleaned_text


def read_email(imap, email_ID):

    read_email = {}

    # fetch the email message by ID
    _, msg = imap.fetch(str(email_ID), "(RFC822)")


    for response in msg:

        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])

            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)


            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)

            
            # decode email receiving time
            Date, encoding = decode_header(msg["Date"])[0]
            if isinstance(Date, bytes):
                Date = Date.decode(encoding)
                
            
            read_email['subject'] = subject
            read_email['from']    = From
            read_email['date']    = Date


            # if the email message is multipart
            if msg.is_multipart():

                # iterate over email parts
                for part in msg.walk():

                    # extract content type of email
                    content_type        = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()

                    except: pass

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # print text/plain emails and skip attachments
                        read_email['body'] = body
                   


            else:
                # extract content type of email
                content_type = msg.get_content_type()

                # get the email body
                body = msg.get_payload(decode=True).decode()

                if content_type == "text/plain":
                    # print only text email parts
                    read_email['body'] = body


    read_email["cleaned_body"] = clean_text(read_email["body"])
    return read_email