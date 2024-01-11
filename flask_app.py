from flask import Flask, render_template, request, redirect, url_for
import feedparser
import schedule
import threading
import time

app = Flask(__name__)

# Separate lists for individual users
SethRSSList = [
    'https://theusawire.com/feed',
    'https://sethconnell.com/feed',
    # Add more Seth's RSS feed URLs as needed
]

JackRSSList = [
    'https://rightwing.org/feed',
    'https://unitedvoice.com/feed',
    # Add more Jack's RSS feed URLs as needed
]

# Global list containing all unique RSS feed URLs without repeats
GlobalRSSList = list(set(SethRSSList + JackRSSList))

def check_rss_feed(rss_list):
    all_user_feed = []
    
    for rss_feed_url in rss_list:
        feed = feedparser.parse(rss_feed_url)

        for entry in feed.entries:
            all_user_feed.append({'headline': entry.title, 'link': entry.link})

    return all_user_feed

@app.route('/')
def home():
    seth_feeds = check_rss_feed(SethRSSList)
    jack_feeds = check_rss_feed(JackRSSList)
    global_feeds = check_rss_feed(GlobalRSSList)
    return render_template('home.html', seth_feeds=seth_feeds, jack_feeds=jack_feeds, global_feeds=global_feeds)

@app.route('/submit_rss', methods=['POST'])
def submit_rss():
    if request.method == 'POST':
        rss_url = request.form.get('seth_rss') or request.form.get('jack_rss')
        if rss_url:
            # Update the respective user's RSS list
            if 'seth_rss' in request.form:
                SethRSSList.append(rss_url)
            elif 'jack_rss' in request.form:
                JackRSSList.append(rss_url)
            
            # Update GlobalRSSList if the URL is not already there
            if rss_url not in GlobalRSSList:
                GlobalRSSList.append(rss_url)
    
    return redirect(url_for('home'))

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # Run the Flask app
    app.run(debug=True, threaded=True)