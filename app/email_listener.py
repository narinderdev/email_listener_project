import imaplib
import email
from email.header import decode_header
import os
from bs4 import BeautifulSoup
from app.config import EMAIL_USER, EMAIL_PASS

def extract_body(msg):
    """
    Extract plain text body from email.message.Message.
    Prefer text/plain, fallback to HTML (converted to text).
    """
    body = ""
    if msg.is_multipart():
        # Try to get text/plain
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                try:
                    body = part.get_payload(decode=True).decode()
                except Exception:
                    body = part.get_payload(decode=True).decode(errors="replace")
                if body.strip():
                    return body
        # Fallback to HTML
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                try:
                    html_body = part.get_payload(decode=True).decode()
                    soup = BeautifulSoup(html_body, "html.parser")
                    text = soup.get_text(separator='\n')
                    if text.strip():
                        return text
                except Exception:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode()
        except Exception:
            body = msg.get_payload(decode=True).decode(errors="replace")
    return body

def check_emails():
    keyword = os.getenv('KEYWORD')
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    typ, data = mail.search(None, 'UNSEEN')
    emails = []
    for num in data[0].split():
        typ, msg_data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        subject, encoding = decode_header(msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        from_addr = msg.get("From")
        body = extract_body(msg)
        # Debug: Print the body for troubleshooting
        print("==== RAW EMAIL BODY ====")
        print(body)
        print("========================")
        if keyword.lower() in subject.lower():
            emails.append({
                "id": num.decode(),
                "subject": subject,
                "from": from_addr,
                "body": body
            })
    mail.logout()
    return emails
