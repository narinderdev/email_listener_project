import keyword
import os
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from app.email_listener import check_emails
from app.parser import parse_email_content
from app.sender import post_data
from app.database import SessionLocal
from app.models import ProcessedEmail
from datetime import datetime

app = FastAPI()
scheduler = BackgroundScheduler()

def job():
    emails = check_emails()
    print(f"Found {len(emails)} new emails")  
    keyword = os.getenv('KEYWORD')
    print(f"Keyword being used: {keyword}")

    db = SessionLocal()
    for mail in emails:
        if not db.query(ProcessedEmail).filter_by(email_id=mail['id']).first():
            parsed = parse_email_content(mail)

            print(f"Parsed data: {parsed}")
            # Post data to endpoint
            import asyncio
            asyncio.run(post_data(parsed))
            # Save to DB
            db.add(ProcessedEmail(
                email_id=mail['id'],
                subject=mail['subject'],
                from_addr=mail['from'],
                received_at=datetime.utcnow(),
                parsed_data=str(parsed)
            ))
            db.commit()
    db.close()

@app.on_event("startup")
def start_scheduler():
    interval = int(os.getenv('POLL_INTERVAL', 10))
    scheduler.add_job(job, 'interval', seconds=interval)
    scheduler.start()

@app.get("/")
def root():
    return {"status": "OK", "msg": "Email listener running"}
