from flask import Flask, request, jsonify, render_template, Response
import mysql.connector
from datetime import datetime
import os
app = Flask(__name__)

db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'CHANGE_ME_IN_PROD'),
    'password': os.environ.get('DB_PASSWORD', 'CHANGE_ME_IN_PROD'),
    'database': os.environ.get('DB_NAME', 'ipblockdb')
}


def get_db_connection():
    return mysql.connector.connect(**db_config)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ips', methods=['GET'])
def list_ips():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT ip_address, blocked_until, reason FROM ip_blocks')
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/ips', methods=['POST'])
def add_or_update_ip():
    data = request.json
    # Obsługa obu formatów dla kompatybilności: lista 'ip_addresses' lub pojedynczy 'ip_address'
    ip_list = data.get('ip_addresses', [])
    single_ip = data.get('ip_address')
    
    if single_ip:
        ip_list.append(single_ip)

    blocked_until = data.get('blocked_until')
    reason = data.get('reason', '')

    if not ip_list or not blocked_until:
        return jsonify({'error': 'ip_addresses list and blocked_until required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    processed_count = 0

    try:
        for ip in ip_list:
            ip = ip.strip() # Usuń spacje
            if not ip: continue

            # Sprawdź czy ip istnieje
            cursor.execute('SELECT blocked_until FROM ip_blocks WHERE ip_address = %s', (ip,))
            row = cursor.fetchone()

            if row:
                # Aktualizuj jeśli nowy blocked_until jest późniejszy
                old_date = row[0]
                # Prosta konwersja stringa na datę
                new_date = datetime.strptime(blocked_until, '%Y-%m-%d %H:%M:%S')

                if old_date is None or old_date < new_date:
                    cursor.execute('UPDATE ip_blocks SET blocked_until = %s, reason = %s WHERE ip_address = %s',
                                   (blocked_until, reason, ip))
            else:
                cursor.execute('INSERT INTO ip_blocks(ip_address, blocked_until, reason) VALUES (%s, %s, %s)',
                               (ip, blocked_until, reason))
            
            processed_count += 1

        conn.commit()
        response = {'status': 'bulk_processed', 'processed_count': processed_count}

    except Exception as e:
        conn.rollback()
        response = {'error': str(e)}
        return jsonify(response), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify(response)


@app.route('/ips/cleanup', methods=['POST'])
def cleanup_expired_ips():
    now = datetime.now()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ip_blocks WHERE blocked_until < %s', (now,))
    deleted = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'deleted_expired': deleted})

@app.route('/blocklist.txt')
def blocklist_txt():
    # Pobierz tylko aktywne blokady
    conn = get_db_connection()
    cursor = conn.cursor()
    # Sprawdzamy, czy blocked_until jest w przyszłości
    cursor.execute('SELECT ip_address FROM ip_blocks WHERE blocked_until > NOW()')
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Wyciągnij same adresy IP z krotek (tuples)
    # results to np. [('1.2.3.4',), ('5.6.7.8',)]
    ip_list = [row[0] for row in results]

    # Połącz je znakiem nowej linii
    text_content = '\n'.join(ip_list)

    # Zwróć jako plik tekstowy (text/plain)
    return Response(text_content, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
