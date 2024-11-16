from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)
api = Api(app)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('DB_NAME', 'brainstorm_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres'),
        port=os.getenv('DB_PORT', '5432')
    )
    return conn

class Vote(Resource):
    def post(self, idea_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT votes FROM ideas WHERE id = %s;", (idea_id,))
        result = cur.fetchone()
        if not result:
            cur.close()
            conn.close()
            return {'message': 'Idea not found.'}, 404

        current_votes = result[0]
        cur.execute("UPDATE ideas SET votes = %s WHERE id = %s;", (current_votes + 1, idea_id))
        conn.commit()
        cur.close()
        conn.close()

        return {'id': idea_id, 'votes': current_votes + 1}, 200

    def get(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, votes FROM ideas;")
        rows = cur.fetchall()
        votes = []
        for row in rows:
            votes.append({
                'id': row[0],
                'votes': row[1]
            })
        cur.close()
        conn.close()
        return jsonify(votes)

api.add_resource(Vote, '/vote/<int:idea_id>', '/votes')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
