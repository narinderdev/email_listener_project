# import pymysql
# import os
# from dotenv import load_dotenv
# from app.models import Base
# from app.database import engine

# load_dotenv()
# db_name = os.getenv("DB_URL").split("/")[-1]  # get db name from URL

# # Connect to mysql server (not the database, just the server)
# # conn = pymysql.connect(
# #     host='db',
# #     port=3308,
# #     user='root',
# #     password='Emaillistener@1'
# # )
# conn = pymysql.connect(
#     host='localhost',
#     port=3306,  # or 3308 if you run MySQL on 3308
#     user='root',
#     password='Emaillistener@1'
# )

# with conn.cursor() as cursor:
#     cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
# conn.close()

# # Now, create tables
# Base.metadata.create_all(bind=engine)
# print("Database and tables created successfully!")
import pymysql
import os
from dotenv import load_dotenv
from app.models import Base
from app.database import engine

load_dotenv()
db_name = os.getenv("DB_URL").split("/")[-1]  # get db name from URL

# Connect to mysql server (not the database, just the server)
# conn = pymysql.connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     password='Emaillistener@1'
# )
conn = pymysql.connect(
    host='db',
    port=3306,
    user='root',
    password='Emaillistener@1'
)
with conn.cursor() as cursor:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
conn.close()

# Now, create tables
Base.metadata.create_all(bind=engine)
print("Database and tables created successfully!")
