import os
import requests
import sqlite3
from bs4 import BeautifulSoup
import cherrypy


class BookmarkScraper:
    def __init__(self, bookmark_file, db_file):
        self.bookmark_file = bookmark_file
        self.db_file = db_file

def scrape(self):
    for bookmark in self.bookmarks:
        url = bookmark['url']
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string.strip()
                print(f"Title of {url} is {title}")
            else:
                print(f"Error: received status code {response.status_code} for {url}")
        except Exception as e:
            print(f"Error occurred for {url}: {e}")


    def scrape(self):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Create the bookmarks table if it doesn't already exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                tags TEXT
            );
        ''')

        # Load the bookmark file
        with open(self.bookmark_file, 'r') as file:
            contents = file.read()

        soup = BeautifulSoup(contents, 'html.parser')

        # Find all <a> tags with a href attribute
        links = soup.find_all('a', href=True)

        for link in links:
            # Extract the URL from the href attribute
            url = link['href']
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                topics = []

                # Extract the relevant content from the website
                content = soup.find_all('p')
                for c in content:
                    # Extract the topics using NLP
                    # Add the topics to the list
                    topics.append(c.get_text())

                # Categorize and tag the website
                # Store the tags in the database
                cursor.execute('''
                    INSERT INTO bookmarks (url, tags) VALUES (?, ?)
                ''', (url, ', '.join(topics)))
            except Exception as e:
                # Add the URL and "error" tag to the database
                cursor.execute('''
                    INSERT INTO bookmarks (url, tags) VALUES (?, ?)
                ''', (url, 'error'))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

class BookmarkApp:
    @cherrypy.expose
    def index(self):
        return '''
            <html>
                <head>
                    <title>Bookmark Scraper</title>
                </head>
                <body>
                    <h1>Bookmark Scraper</h1>
                    <form action="/upload" method="post" enctype="multipart/form-data">
                        <input type="file" name="bookmark_file">
                        <button type="submit">Upload</button>
                    </form>
                </body>
            </html>
        '''

    @cherrypy.expose
    def upload(self, bookmark_file):
        # Save the uploaded file to disk
        save_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(save_path, 'bookmarks.html')
        with open(file_path, 'wb') as f:
            while True:
                data = bookmark_file.file.read(8192)
                if not data:
                    break
                f.write(data)

        # Scrape the bookmarks and store the tags in the database
        scraper = BookmarkScraper(file_path, 'bookmarks.db')
        scraper.scrape()

        # Redirect the user to the bookmarks page
        raise cherrypy.HTTPRedirect('/bookmarks')


@cherrypy.expose
def bookmarks(self):
    # Connect to the SQLite database and retrieve all bookmarks
    # Connect to the SQLite database and retrieve all bookmarks
    conn = sqlite3.connect('bookmarks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT url, tags FROM bookmarks')
    bookmarks = cursor.fetchall()

    # Generate HTML for displaying the bookmarks and their tags
    html = '''
            <html>
                <head>
                    <title>Bookmarks</title>
                </head>
                <body>
                    <h1>Bookmarks</h1>
                    <table>
                        <tr>
                            <th>URL</th>
                            <th>Tags</th>
                        </tr>
        '''
    for bookmark in bookmarks:
        url, tags = bookmark
        html += f'''
                    <tr>
                        <td><a href="{url}">{url}</a></td>
                        <td>{tags}</td>
                    </tr>
                '''
    html += '''
                    </table>
                </body>
            </html>
        '''
    return html


if __name__ == '__main__':
    cherrypy.quickstart(BookmarkApp())
