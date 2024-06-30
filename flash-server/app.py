from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname='api_hit_tracking', 
        user='api_user', 
        password='password', 
        host='localhost'
    )
    return conn

# Route to track API hits
@app.route('/track', methods=['GET', 'POST', 'PUT', 'DELETE'])
def track():
    req_data = {
        'request_id': request.args.get('id'),
        'request_type': request.method,
        'request_time': datetime.now(),
        'payload': request.get_data(as_text=True),
        'content_type': request.headers.get('Content-Type'),
        'ip_address': request.remote_addr,
        'operating_system': request.headers.get('User-Agent').split('(')[1].split(')')[0],
        'user_agent': request.headers.get('User-Agent')
    }

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO api_hits (request_id, request_type, request_time, payload, content_type, ip_address, operating_system, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (req_data['request_id'], req_data['request_type'], req_data['request_time'], req_data['payload'], req_data['content_type'], req_data['ip_address'], req_data['operating_system'], req_data['user_agent'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success'}), 200

# Route to fetch API hits
@app.route('/hits', methods=['GET'])
def get_hits():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_hits")
    hits = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(hits), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
