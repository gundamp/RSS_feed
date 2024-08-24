import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timezone
import schedule
import time

# Function to fetch and filter the RSS feeds from multiple websites
def fetch_and_filter_feed():
    urls = [
        'https://realpython.com/atom.xml',
        #'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',  # Add more URLs here
        # Add more URLs as needed
    ]
    
    filtered_entries = []
    
    start_date = datetime(2024, 8, 23)
    end_date = datetime(2024, 8, 31)
    
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        entries = soup.find_all('entry')
    
        for entry in entries:
            title = entry.title.text
            summary = entry.summary.text
            link = entry.link['href']
            date = datetime.strptime(entry.updated.text, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)  # Strip timezone

            if start_date <= date <= end_date:
                filtered_entries.append(f"Title: {title}\n\nSummary: {summary}\n\nLink: {link}\n\nDate: {date}\n\n")
    
    return filtered_entries

# Function to send email
def send_email(entries):
    from_email = "youremail@outlook.com"
    to_email = "youremail@hotmail.com"
    subject = "Daily RSS Feed"
    body = "\n\n".join(entries)

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # SMTP session
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(from_email, 'yourpassword')
    text = message.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

# Function to perform the entire process
def daily_email():
    entries = fetch_and_filter_feed()
    if entries:
        send_email(entries)
    else:
        print("No new entries to send.")

# Schedule the task to run daily at a specific time
schedule.every().day.at("10:21").do(daily_email)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)