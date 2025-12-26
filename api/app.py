from flask import Flask, request, jsonify
import sqlite3
import bcrypt
hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

app = Flask(__name__)

DATABASE = "users.db"

# ----------------------------------
# Connexion à la base de données
# ----------------------------------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

# ----------------------------------
# Route LOGIN (SQL sécurisé)
# ----------------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Validation des entrées
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Invalid input"}), 400

    username = data["username"]
    password = data["password"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Requête SQL paramétrée (ANTI SQL INJECTION)
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success", "user": username})

    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

# ----------------------------------
# Route HELLO (test)
# ----------------------------------
@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "DevSecOps API running securely"})

# ----------------------------------
# Lancement de l'application
# ----------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
