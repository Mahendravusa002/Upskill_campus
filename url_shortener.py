import string
import random
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DATABASE = 'url_shortener.db'

# Function to create a shortened URL
def generate_short_url():
    chars = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(chars) for _ in range(6))
    return short_url

# Function to store the mapping between original and shortened URLs
def save_url_mapping(original_url, short_url):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)",
              (original_url, short_url))
    conn.commit()
    conn.close()

# Function to retrieve the original URL from the shortened URL
def get_original_url(short_url):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT original_url FROM urls WHERE short_url=?", (short_url,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

# Home page route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_url = generate_short_url()
        save_url_mapping(original_url, short_url)
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

# Redirect route
@app.route('/<short_url>')
def redirect_to_original_url(short_url):
    original_url = get_original_url(short_url)
    if original_url:
        return redirect(original_url)
    return "URL not found."

if __name__ == '__main__':
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, original_url TEXT, short_url TEXT)")
    conn.commit()
    conn.close()
    app.run(debug=True)
