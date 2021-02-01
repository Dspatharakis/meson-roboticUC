from flask import Flask
import requests

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

app.run()
