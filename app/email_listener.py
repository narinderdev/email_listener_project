import imaplib
import email
import os
from email.header import decode_header
from app.config import EMAIL_USER, EMAIL_PASS


def check_emails():
    keyword = os.getenv('KEYWORD')
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    typ, data = mail.search(None, f'(UNSEEN SUBJECT "{keyword}")')
    emails = []
    for num in data[0].split():
        typ, msg_data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        subject, encoding = decode_header(msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        from_addr = msg.get("From")
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    try:
                        body = part.get_payload(decode=True).decode()
                    except Exception:
                        body = part.get_payload(decode=True).decode(errors="replace")
                    break
            # Fallback for HTML
            if not body:
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        try:
                            body = part.get_payload(decode=True).decode()
                            break
                        except Exception:
                            pass
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except Exception:
                body = msg.get_payload(decode=True).decode(errors="replace")
        emails.append({
            "id": num.decode(),
            "subject": subject,
            "from": from_addr,
            "body": body
        })
    mail.logout()
    return emails
