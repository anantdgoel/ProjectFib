import os
from flask import Flask, request
from flask.ext.cors import CORS, cross_origin
from imageverify import main

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def hello():
    user = request.args.get('content')
    status = main(user)
    return status

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
