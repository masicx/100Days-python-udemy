import requests, smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "B7FWWZBYWBSJG0ML"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data_json = response.json()

yesterday_data = data_json["Time Series (Daily)"][list(data_json["Time Series (Daily)"].keys())[0]]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_json["Time Series (Daily)"][list(data_json["Time Series (Daily)"].keys())[1]]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
percentage = round(difference / float(yesterday_closing_price) * 100, 2)

if percentage > 5:
    print("Get News")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
news_data = []
if abs(percentage) > 1:
    news_params = {
        "apiKey": "492bcf49cd1e49b3929848d097c73fd3",
        "qInTitle": COMPANY_NAME
    }

    news_response = requests.get("https://newsapi.org/v2/everything", params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]

    for article in news_data:
        print(f"Headline: {article['title']}. \nBrief: {article['description']}")
## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number. 
with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user="masicx@gmail.com", password="ktqs lfhj tjml diux")
    for article in news_data:
        connection.sendmail(
            from_addr="masicx@gmail.com", 
            to_addrs="salo33_@hotmail.com", 
            # msg=f"Subject: {STOCK} has changed: {up_down}{percentage}%\n\nHeadline: {article['title']}. \nBrief: {article['description']}")
            msg=f"Subject: {STOCK} has changed: {percentage}%\n\nHeadline: {article['title']}. \nBrief: {article['description']}")

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

