from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "devops"),
        user=os.getenv("DB_USER", "devops"),
        password=os.getenv("DB_PASSWORD", "devops")
    )

@app.route("/health")
def health():
    return {"status": "ok"}
@app.route("/data")
def data():
    return jsonify({
        "name": "devops-lab",
        "version": 1
    })

@app.route("/time")
def time():
    return {
        "server_time": str(datetime.datetime.now())
    }

@app.route("/db-check")
def db_check():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        conn.close()

        return {"db": "connected", "result": result}
    except Exception as e:
        return {"db": "failed", "error": str(e)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)