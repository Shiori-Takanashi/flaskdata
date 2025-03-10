from flask import Flask, Response
import sqlite3
import json
from flask_cors import CORS

app = Flask(__name__)

DATABASE = 'db.sqlite3'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    # UTF-8でデコード（エラー発生時は置換）
    conn.text_factory = lambda b: b.decode("utf-8", errors="replace")
    return conn

@app.route('/random', methods=['GET'])
def get_random_data():
    conn = get_db_connection()
    query = '''
        SELECT DISTINCT *
        FROM pokedex_pokemon
        WHERE original = 1
        ORDER BY RANDOM() LIMIT 1
    '''
    cur = conn.execute(query)
    row = cur.fetchone()
    conn.close()

    if row:
        data = dict(row)
        # ensure_ascii=False で日本語がエスケープされずに出力される
        response_body = json.dumps(data, ensure_ascii=False)
        return Response(response_body, content_type="application/json; charset=utf-8")
    else:
        response_body = json.dumps({"error": "データが見つかりません"}, ensure_ascii=False)
        return Response(response_body, content_type="application/json; charset=utf-8", status=404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
