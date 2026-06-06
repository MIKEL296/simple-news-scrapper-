from flask import Flask, render_template, redirect, url_for
from scrapper import NewsScraperModel

app = Flask(__name__)

# Temporary in-memory "database" to hold articles between requests
stored_articles = []

@app.route('/')
def index():
    # Renders the HTML page, passing in whatever articles we have stored
    return render_template('index.html', articles=stored_articles)

@app.route('/scrape', methods=['POST'])
def scrape():
    global stored_articles
    # Tell the model to fetch fresh data
    stored_articles = NewsScraperModel.get_hacker_news()
    # Redirect back to the main homepage to display the updates
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Runs the local development server
    app.run(debug=True, port=5000)