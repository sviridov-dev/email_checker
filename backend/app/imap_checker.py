from itertools import count
from imap_tools import MailBox, AND
import imaplib  # for specific IMAP errors
from datetime import datetime, timezone
from imapclient import IMAPClient
from email.utils import parsedate_to_datetime
from email import policy
from email.parser import BytesParser

def check_email_status(gmail_email, app_password, from_email_or_name):
    result = {"inbox": False, "spam": False, "not_found": True, "diff_time": ""}
    
    # List of folders to search
    folders = ["INBOX", "[Gmail]/Spam"]

    def short_date(date):
        
        try:
            if date is None:
                return ""
            now = datetime.now()
            diff = now - date
            if diff.total_seconds() < 60:
                return "Just now"
            elif diff.total_seconds() < 3600:
                return f"{int(diff.total_seconds() // 60)} minutes ago"
            elif diff.total_seconds() < 86400:
                return f"{int(diff.total_seconds() // 3600)} hours ago"
            else:
                return f"{diff.days} days ago"
        except Exception as e:
            return "Unknown"
        
    def find_email():
        try:
            
            def fetch_emails(client, folder, search_text, limit):
                client.select_folder(folder)
                criteria = ['ALL'] if not search_text else ['FROM', search_text]
                uids = client.search(criteria)
                uids = uids[-limit:]  # take last `limit` emails
                messages = client.fetch(uids, ['ENVELOPE', 'X-GM-LABELS'])
                results = []
                for uid, data in messages.items():
                    envelope = data[b'ENVELOPE']
                    subject = envelope.subject.decode() if envelope.subject else "(No subject)"
                    sender = f"{envelope.from_[0].mailbox.decode()}@{envelope.from_[0].host.decode()}"
                    sender_name = envelope.from_[0].name.decode() if envelope.from_[0].name else "(No name)"

                    labels = [l.decode() for l in data.get(b'X-GM-LABELS', [])]
        
                    # Fetch full raw email for body parsing
                    raw_data = client.fetch([uid], ['RFC822'])[uid][b'RFC822']
                    msg = BytesParser(policy=policy.default).parsebytes(raw_data)
                    
                    # Extract plain text and html bodies
                    text_body = None
                    html_body = None
                    if msg.is_multipart():
                        for part in msg.walk():
                            ct = part.get_content_type()
                            if ct == "text/plain" and text_body is None:
                                text_body = part.get_content()
                            elif ct == "text/html" and html_body is None:
                                html_body = part.get_content()
                    else:
                        if msg.get_content_type() == "text/plain":
                            text_body = msg.get_content()
                        elif msg.get_content_type() == "text/html":
                            html_body = msg.get_content()
                    results.append({
                        "folder": folder,
                        "date": envelope.date,
                        "sender": sender,
                        "sender_name": sender_name,
                        "subject": subject,
                        "labels": [l.decode() for l in data.get(b'X-GM-LABELS', [])],
                        "text_body": text_body,
                        "html_body": html_body
                    })
                return results
                        
            with IMAPClient('imap.gmail.com', port=993, ssl=True) as client:
                client.login(gmail_email, app_password)
                
                inbox_emails = fetch_emails(client, "INBOX", from_email_or_name, 10)
                spam_emails = fetch_emails(client, "[Gmail]/Spam", from_email_or_name, 10)
                
                all_emails = inbox_emails + spam_emails
                # Sort combined by date (newest first)
                all_emails.sort(key=lambda x: x['date'], reverse=True)

                return [{"folder": "INBOX", "emails": inbox_emails}, {"folder": "SPAM", "emails": spam_emails}]



            

        except imaplib.IMAP4.error as e:
            print(f"IMAP error occurred while accessing folder : {e}")
            return False
        except Exception as e:
            print(f"Unexpected error while accessing folder : {e}")
            return False

    # Loop through each folder
    results = []
    # Check each folder for the email
    # results = [{"inbox": 0, "spam": 0, "not_found": 0, "diff_time": "", "text": "", "sender": ""}]
    inbox_count = 0
    spam_count = 0  


        
    received_list = find_email()  # Pass the folder variable here


    if received_list == False:
        return {'results':[], 'inbox': 0, 'spam': 0, 'not_found': 1, 'type': 'invalid'}

    for received in received_list:
        email_count = 0
        for email in received['emails']:
            email_count += 1
            result = {}
            result["type"] = "inbox" if received['folder'] == "INBOX" else "spam"
            result["diff_time"] = short_date(email['date'])
            result["date"] = email['date']
            result["text"] = email['text_body']
            result["subject"] = email['subject']
            result["sender_email"] = email['sender']
            result["sender_name"] = email['sender_name']
            results.append(result)
        # Count emails in each folder
        inbox_count += email_count if received['folder'] == "INBOX" else 0
        spam_count += email_count if received['folder'] == "SPAM" else 0

    return {'results': results, 'email': gmail_email, 'inbox': inbox_count, 'spam': spam_count, 'not_found': 0 if inbox_count + spam_count > 0 else 1, 'type': 'valid'}
