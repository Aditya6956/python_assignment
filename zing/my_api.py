from flask import Flask, request, jsonify
from flask_restful import Api
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'stock_price'
mysql = MySQL(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/api/v1/resources/stocks/all', methods=['GET','POST'])
def api_all():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute('SELECT * FROM stock_price.bhavcopy;')
    all_stocks = cur.fetchall()
    return jsonify(all_stocks)

@app.route('/api/v1/resources/stocks', methods=['GET','POST'])
def api_filter():
    query_parameters = request.args

    symbol = query_parameters.get('symbol')
    isin = query_parameters.get('isin')

    query = "SELECT * FROM bhavcopy WHERE"
    to_filter = []

    if symbol:
        query += ' symbol=%s AND'
        to_filter.append(symbol)
    if isin:
        query += ' isin=%s AND'
        to_filter.append(isin)
    
    print(to_filter)

    if not (id or symbol or isin):
        return "Null"

    query = query[:-4] + ';'

    conn = mysql.connection
    cur = conn.cursor()
    
    cur.execute(query, to_filter)   
    results = cur.fetchall()

    return jsonify(results)

@app.route('/api/v1/resources/stocks_details', methods=['GET'])
def get_data():
    query_parameters = request.args

    symbol = query_parameters.get('symbol')
    isin = query_parameters.get('isin')

    query = "SELECT * FROM equity WHERE"
    to_filter = []

    if symbol:
        query += ' symbol=%s AND'
        to_filter.append(symbol)
    if isin:
        query += ' isin_number=%s AND'
        to_filter.append(isin)

    query = query[:-4] + ';'

    conn = mysql.connection
    cur = conn.cursor()
    
    cur.execute(query, to_filter)   
    results = cur.fetchall()

    return jsonify(results)

if __name__ == '__main__':
    app.run()