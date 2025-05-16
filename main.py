from flask import Flask, Response, render_template, send_from_directory
import sqlite3
import json
from flask_cors import CORS
import time, random

app = Flask(__name__, static_folder=None)

CORS(app)

DATABASE = 'db.sqlite3'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.text_factory = lambda b: b.decode("utf-8", errors="replace")
    return conn

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/assets/<path:filename>")
def serve_asset(filename):
    return send_from_directory("static_assets", filename)

@app.route("/sample/<path:filename>")
def serve_sample(filename):
    return send_from_directory("static_sample", filename)

@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory("static_css", filename)

@app.route("/webfonts/<path:filename>")
def serve_webfonts(filename):
    return send_from_directory("static_webfonts", filename)


@app.route('/random', methods=['GET'])
def get_random_data():
    conn = get_db_connection()
    query = '''
        SELECT *
        FROM pokedex_pokemon
        WHERE original = 1
        ORDER BY RANDOM()
        LIMIT 1
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

@app.route('/species/<int:idx>', methods=['GET'])
def get_species_by_id(idx):
    idx_str = str(idx).zfill(5)

    conn = get_db_connection()
    query = 'SELECT * FROM pokedex_pokemon WHERE species_id = ?'
    cur = conn.execute(query, (idx_str,))
    row = cur.fetchone()
    conn.close()

    if row:
        data = dict(row)
        response_body = json.dumps(data, ensure_ascii=False)
        return Response(response_body, content_type="application/json; charset=utf-8")
    else:
        response_body = json.dumps({'error': '指定されたIDのデータが見つかりません'}, ensure_ascii=False)
        return Response(response_body, content_type="application/json; charset=utf-8", status=404)

@app.route('/species/delay/<int:idx>', methods=['GET'])
def get_species_by_id_with_delay(idx):
    idx_str = str(idx).zfill(5)

    conn = get_db_connection()
    query = 'SELECT * FROM pokedex_pokemon WHERE species_id = ?'
    cur = conn.execute(query, (idx_str,))
    row = cur.fetchone()
    conn.close()

    time.sleep(random.randint(3,6))

    if row:
        data = dict(row)
        response_body = json.dumps(data, ensure_ascii=False)
        return Response(response_body, content_type="application/json; charset=utf-8")
    else:
        response_body = json.dumps({'error': '指定されたIDのデータが見つかりません'}, ensure_ascii=False)
        return Response(response_body, content_type="application/json; charset=utf-8", status=404)
