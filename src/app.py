import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from rsa import RSA
from signature import Signature
import io
import re
import ast

# Flask Configuration.
app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'mysecret'


"""
--------------------------------------------------------------
# Default Route
--------------------------------------------------------------
"""
# @app.route("/")
# def index():
#     return render_template("index.html")

	

"""
--------------------------------------------------------------
# Route for Home
--------------------------------------------------------------
"""
# Index route.
@app.route("/")
def index():
    return render_template("index.html")

"""
--------------------------------------------------------------
# Route for Generate Public Key
--------------------------------------------------------------
"""
# Sign Route
@app.route("/generate", methods=['POST','GET'])
def generate():
    if request.method == 'POST':
        key = RSA.generateKey()
        public_key = key[0]
        private_key = key[1]
        return render_template("generate.html", public = public_key, private = private_key)
    else:
        return render_template("generate.html")


"""
--------------------------------------------------------------
# Route for Signing Documents
--------------------------------------------------------------
"""
# Sign Route
@app.route("/sign", methods=['POST','GET'])
def sign():
    if request.method == 'POST':
        d = int(request.form['text1'])
        n = int(request.form['text2'])
        text = request.form['text3']
        result = Signature.sign(text, [d,n])
        return render_template("sign.html", d=d, n=n, document=text, signed=result)
    else:
        return render_template("sign.html")

"""
--------------------------------------------------------------
# Route for Verifying Documents
--------------------------------------------------------------
"""
# Sign Route
@app.route("/verify", methods=['POST','GET'])
def verify():
    if request.method == 'POST':
        e = int(request.form['text1'])
        n = int(request.form['text2'])
        text = request.form['text3']
        try:
            result = Signature.verify(text, [e,n])
            if(result):
                result = "Document Verified"
            else:
                result = "Document Not Verified"
            return render_template("verify.html", e=e, n=n, signed_document=text, status=result)
        except:
            return render_template("verify.html", e=e, n=n, signed_document=text, status="Document Not Verified")

    else:
        return render_template("verify.html")

"""
--------------------------------------------------------------
# Route for Utility
--------------------------------------------------------------
"""
@app.route("/saveresult", methods=['POST'])
def saveResult():
    result = request.form['result']
    return send_file(io.BytesIO(result.encode()), mimetype="text/plain",as_attachment=True, attachment_filename="result.txt")

@app.route("/savepublickey", methods=['POST'])
def savePublicKey():
    result = request.form['public']
    return send_file(io.BytesIO(result.encode()), mimetype="text/plain",as_attachment=True, attachment_filename="example_public_key.pub")

@app.route("/saveprivatekey", methods=['POST'])
def savePrivateKey():
    result = request.form['private']
    return send_file(io.BytesIO(result.encode()), mimetype="text/plain",as_attachment=True, attachment_filename="example_private_key.pri")

"""
--------------------------------------------------------------
# Flask Main Program
--------------------------------------------------------------
"""
if __name__ == '__main__':
	app.run(debug=True,threaded=True)

