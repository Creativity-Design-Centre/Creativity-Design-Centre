from ontology import app
from search import search, google_image
from flask import request
import requests
import json


@app.route('/')
def hello_world():
    concept_request = requests.get('http://api.conceptnet.io/c/en/aaa').json()
    return concept_request


@app.route('/search')
def serach_query():
    keyword = request.args.get('keyword')
    rlt_all = search.search_concept(keyword)
    rlt_dtl = rlt_all.query_result()
    return rlt_dtl


@app.route('/get_image')
def search_image():
    keyword = request.args.get('keyword')
    get_image = google_image.search_image(keyword)
    rlt = get_image.get_image()
    return {
        'errno': 0,
        'errmsg': '',
        'data': rlt
    }
