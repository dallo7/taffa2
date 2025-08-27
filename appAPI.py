import os
from flask import Flask, jsonify, request, g
import sqlite3

# Initialize the Flask app
app = Flask(__name__)
app.config['DATABASE'] = 'tra_cfa_data.db'


# --- Database Connection and Resource Management ---
def get_db():
    """Establishes and returns a new database connection for the current request."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# --- API Endpoint ---

@app.route('/Taffa/check-urn', methods=['GET'])
def check_urn_existence():
    """
    API endpoint to check if a particular URN exists in the system.
    Returns a simple boolean response.

    Expected URL: /check-urn?urn=<URN>
    """
    urn = request.args.get('urn')

    if not urn:
        return jsonify({"error": "Please provide a 'urn' parameter."}), 400

    db = get_db()
    cursor = db.cursor()

    try:
        # Query the database to check for the URN
        sql_query = """
            SELECT EXISTS(SELECT 1 FROM consignments WHERE urn = ? LIMIT 1)
        """
        cursor.execute(sql_query, (urn,))
        urn_exists = cursor.fetchone()[0] == 1

        return jsonify({
            "urn_exists": urn_exists
        }), 200

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


# --- Main execution block ---
if __name__ == '__main__':
    if not os.path.exists('tra_cfa_data.db'):
        print("Database file 'tra_cfa_data.db' not found. Please run the Dash app to create it.")
    else:
        app.run(debug=True, port=5057)