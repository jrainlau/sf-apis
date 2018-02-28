from flask import Flask
from sf import get_articles
import json

app = Flask(__name__)

artilce_list = get_articles()

@app.route('/list')
def get_articles():
    return json.dumps(artilce_list, indent = 2, ensure_ascii=False)

if __name__ == '__main__':
    app.run()
