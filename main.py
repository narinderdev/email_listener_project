import os
import json
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from app.email_listener import check_emails
from app.parser import parse_email_content
from app.sender import post_data
from app.database import SessionLocal
from app.models import ProcessedEmail
from datetime import datetime
import asyncio

app = FastAPI()
scheduler = BackgroundScheduler()

def job():
    emails = check_emails()
    print(f"Found {len(emails)} new emails")  
    keyword = os.getenv('KEYWORD')
    print(f"Keyword being used: {keyword}")

    db = SessionLocal()
    try:
        for mail in emails:
            parsed = parse_email_content(mail)
            parsed_json = json.dumps(parsed, sort_keys=True)

            last_entry = db.query(ProcessedEmail).order_by(ProcessedEmail.id.desc()).first()
            if last_entry:
                try:
                    last_parsed_dict = json.loads(last_entry.parsed_data)
                    last_parsed_json = json.dumps(last_parsed_dict, sort_keys=True)
                except Exception:
                    last_parsed_json = None
            else:
                last_parsed_json = None

            if last_parsed_json == parsed_json:
                print("No data change detected (duplicate parsed fields). Skipping save.")
                continue

            print(f"Parsed data: {parsed}")
            # Post data to endpoint
            try:
                asyncio.run(post_data(parsed))
            except Exception as e:
                print(f"Error posting data: {e}")
            # Save to DB
            db.add(ProcessedEmail(
                email_id=mail['id'],
                subject=mail['subject'],
                from_addr=mail['from'],
                received_at=datetime.utcnow(),
                parsed_data=parsed_json
            ))
            db.commit()

    except Exception as e:
        print(f"Error processing emails: {e}")
        db.rollback()  # This is safe, even if nothing to roll back
    finally:
        db.close()

@app.on_event("startup")
def start_scheduler():
    interval = int(os.getenv('POLL_INTERVAL', 10))
    scheduler.add_job(job, 'interval', seconds=interval)
    scheduler.start()

@app.get("/")
def root():
    return {"status": "OK", "msg": "Email listener running"}
