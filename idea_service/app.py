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

class Idea(Resource):
    def post(self):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')

        if not title or not description:
            return {'message': 'Title and Description are required.'}, 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO ideas (title, description, votes) VALUES (%s, %s, %s) RETURNING id;",
            (title, description, 0)
        )
        idea_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {'id': idea_id, 'title': title, 'description': description, 'votes': 0}, 201

    def get(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, description, votes FROM ideas;")
        rows = cur.fetchall()
        ideas = []
        for row in rows:
            ideas.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'votes': row[3]
            })
        cur.close()
        conn.close()
        return jsonify(ideas)

api.add_resource(Idea, '/ideas')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
