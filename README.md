# Email Listener Project
1.Clone the repository
git clone https://github.com/yourusername/fastapi-email-listener.git
cd fastapi-email-listener

2.Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

3.Install dependencies
pip install -r requirements.txt

4.Create a .env file in the root directory with the following variables:

EMAIL_USER=your_gmail_address@gmail.com
EMAIL_PASS=your_app_password_or_gmail_password
KEYWORD=app             # Subject keyword filter
DB_URL=mysql+pymysql://root:password@localhost:3306/email_listener
ENDPOINT_URL=https://yourtargetapi.com/post-endpoint
POLL_INTERVAL=60        # Poll interval in seconds

5.Initialize database

Make sure your MySQL database is running and create the email_listener database.

Apply migrations or run your SQLAlchemy model setup code to create tables.

6.Running the App
Locally:uvicorn main:app --reload

7.Using Docker:docker-compose up --build


How It Works:
1.The app connects to the Gmail IMAP server and looks for unread emails with the subject containing your keyword (KEYWORD).

2.It parses the email body to extract relevant info using regex or custom logic.

3.Saves the email metadata and parsed data into the MySQL database.

4.Posts the parsed data as JSON to the ENDPOINT_URL.

5.Runs this process repeatedly every POLL_INTERVAL seconds using APScheduler.