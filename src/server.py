#!/usr/bin/env python

from flask import Flask, url_for, request, Response
from newspaper import Article
import os, json
import requests
from dragnet.util import load_pickled_model

app = Flask(__name__)
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

content_extractor = load_pickled_model('kohlschuetter_readability_weninger_comments_content_model.pkl.gz')

@app.route('/', methods = ['GET'])
def metrics():  # pragma: no cover
    content = open('/index.html').read()
    return Response(content, mimetype="text/html")

@app.route('/topimage',methods = ['GET'])
def api_top_image():
    url = request.args.get('url')
    article_content = download_article(url)
    # Get most article information from newspaper
    article = get_article(url, article_content)
    # Get text content from dragnet
    dragnet_text = get_dragnet_text(article_content)
    return json.dumps({
        "authors": article.authors,
        "images:": list(article.images),
        "movies": article.movies,
        "publish_date": article.publish_date.strftime("%s") if article.publish_date else None,
        "text": dragnet_text,
        "title": article.title,
        "topimage": article.top_image}), 200, {'Content-Type': 'application/json'}

@app.route('/oldApi',methods = ['GET'])
def old_api():
    url = request.args.get('url')
    r = requests.get("http://newspaper-api.smarpsocial.com:38765", params={'url': url})
    return r.text

def download_article(url):
    r = requests.get(url)
    return r.content

def get_dragnet_text(content):
    return content_extractor.extract(content)

def get_article(url, input_html):
    article = Article(url, request_timeout=20)
    article.download(input_html = input_html)
    # uncomment this if 200 is desired in case of bad url
    # article.set_html(article.html if article.html else '<html></html>')
    article.parse()
    return article

if __name__ == '__main__':
    port = os.getenv('NEWSPAPER_PORT', '38765')
    app.run(port=int(port), host='0.0.0.0')
