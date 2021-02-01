from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def notify_pp_and_iu():
    content = request.json
    print('Notifying Path Planner to skip position', content['position'], 'in next mission.')
    print('Notifying Inventory Unloader to initiate CSC actions to load position', content['position'])
    return 'Successfully Notified all partied involved!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)