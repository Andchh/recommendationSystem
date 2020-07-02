from flask import Flask, jsonify, request
import pandas as pd
from Purchase import Purchase

app = Flask(__name__)
add_product = Purchase()

@app.route('/')
def home():
    return "http://127.0.0.1:5000/recommendations"

@app.route('/recommendations', methods=['GET'])
def recommendations():
    output = pd.read_csv('output.csv', sep = ";")
    output.set_index(['COD_CLIENTE'], inplace=False)
    return output.to_html(), 200


@app.route('/recommendations/<string:user_id>', methods=['GET'])
def recom_per_user(user_id):
    output = pd.read_csv('output.csv', sep = ";")
    index = output[output['COD_CLIENTE']==user_id].index.values
    print("o index eh", index)
    if (len(index) == 0):
        return jsonify({'error':'not found'}), 404
    else:
        client = output[output.index == index[0]]
        return client.to_html(), 200


@app.route('/purchase/add', methods=['POST'])
def add_purchase():
    entry = request.get_json()
    status = add_product.add(entry)
    return status


if __name__ == '__main__':
    app.run(debug=True, port=5000)