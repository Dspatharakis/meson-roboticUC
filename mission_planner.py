from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def unload():
    with open("unload.txt", "w") as f:
        f.write("This is Test Data")

    return 'Unload Complete!'

@app.route('/renew_db')
def renew_db():
    with open("unload.txt", "w") as f:
       return 'Renew Complete!'

@app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    print(content['mytext'])
    return jsonify({"uuid":uuid})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
