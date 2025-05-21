import re

def parse_email_content(body):
    # Example: Extract a code or field from email body
    result = re.search(r"Order ID: (\d+)", body)
    return {"order_id": result.group(1) if result else None}
