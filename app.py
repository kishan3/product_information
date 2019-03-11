import requests
from flask import Flask, jsonify, request

from credentials import FP_AFFILIATE_TRACKING_ID, FP_Token, API_URL

app = Flask(__name__)


def remove_duplicates(products, query):
    unique_products = []
    query_seen = False
    for product in products:
        if query in product['productBaseInfoV1']['title'].lower() and not query_seen:
            unique_products.append(product)
            query_seen = True
    return unique_products


@app.route('/search')
def search_products():
    headers = {"Fk-Affiliate-Id": FP_AFFILIATE_TRACKING_ID, "Fk-Affiliate-Token": FP_Token}
    query = request.values.get('query')
    print(request.values)
    response = requests.get(API_URL.format(query),
                            headers=headers)
    if response.status_code == 200 and response.ok:
        response = response.json()
        products = response['products']
        unique_products = remove_duplicates(products, query)
        return jsonify({'result': unique_products})
    return jsonify({'result': []})
