from flask import Flask, request
from sf import get_articles
import json

app = Flask(__name__)

@app.route('/getArticleList.json')
def articlesList():
    return json.dumps(get_articles(request), indent = 2, ensure_ascii = False)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
