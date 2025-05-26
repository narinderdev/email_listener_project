import re
from email.utils import parseaddr

def parse_email_content(mail):
    body = mail.get('body', '')
    from_addr = mail.get('from', '')

    # Normalize newlines and spaces
    body = body.replace('\r\n', '\n')
    body = re.sub(r'[ \t]+', ' ', body)

    print("==== RAW EMAIL BODY ====")
    print(body)
    print("========================")

    # Sender info
    _, sender_email = parseaddr(from_addr)

    # 1. Extract Customer Rep (case-insensitive)
    rep_match = re.search(r"Customer\s*Rep:\s*(.*)", body, re.IGNORECASE)
    customer_rep = rep_match.group(1).strip() if rep_match else None

    # 2. MOVING FROM block (case-insensitive)
    moving_from_section = ""
    try:
        moving_from_section = re.search(r"MOVING FROM(.*?)RELOCATION DETAILS", body, re.DOTALL | re.IGNORECASE).group(1)
    except AttributeError:
        pass

    # 3. Phone numbers (case-insensitive)
    phone_matches = re.findall(r"Phone:\s*(\d+)", moving_from_section, re.IGNORECASE)
    phone1 = phone_matches[0] if len(phone_matches) > 0 else None
    phone2 = phone_matches[1] if len(phone_matches) > 1 else None

    # 4. Contact email under MOVING FROM only
    email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-zA-Z]{2,}\b", moving_from_section)
    contact_email = email_match.group(0) if email_match else None

    # Extract Customer Payment amount (case-insensitive)
    payment_match = re.search(r"Customer\s+Payment:.*?\$([\d,]+\.\d{2})", body, re.DOTALL | re.IGNORECASE)
    customer_payment = payment_match.group(1).replace(',', '') if payment_match else None

    return {
        "repName": customer_rep,
        "email": contact_email,
        "phone1": phone1,
        "phone2": phone2,
        "customerPayment": customer_payment
    }
