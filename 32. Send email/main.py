import smtplib, random
from datetime import datetime
import dotenv
import os

dotenv.load_dotenv()

PASSWORD = str(os.environ.get("EMAIL_PASSWORD"))
EMAIL_TO = str(os.environ.get("EMAIL_TO"))

def get_quotes():
    with open(r"C:\Code\100DaysCourse\32. Send email\quotes.txt", "r") as file:
        quotes = file.readlines()
        return quotes

quotes = get_quotes()
random_quote = random.choice(quotes)
if datetime.now().weekday() == 5:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("masicx@gmail.com", PASSWORD)
        server.sendmail(
            from_addr="masicx@gmail.com", 
            to_addrs=EMAIL_TO, 
            msg=f"Subject: Hello\n\n{random_quote}")
    
# with smtplib.SMTP("smtp.gmail.com", 587) as server:
#     server.starttls()
#     server.login("masicx@gmail.com", PASSWORD)
#     server.sendmail(
#         from_addr="masicx@gmail.com", 
#         to_addrs="masicx@gmail.com", 
#         msg="Subject: Hello\n\nThis is the body of my email.")

# import datetime

# now = datetime.datetime.now()
# year = now.year
# print(now.weekday())

# date_of_birth = datetime.datetime(year=1990, month=6, day=25)
# print(date_of_birth)

