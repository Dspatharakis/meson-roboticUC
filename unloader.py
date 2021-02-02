from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/update_db', methods=['GET', 'POST'])
def update_db():