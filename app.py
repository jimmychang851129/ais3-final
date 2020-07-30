from flask import Flask, render_template, flash, redirect, url_for, jsonify
import os
from flask import request
import utils
import Config as cm

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/HMIquery',methods=['POST','GET'])
def handleHMIRequest():
	level = request.form.get('HMIquery')
	key = "c"*16	# tmp
	return jsonify(utils.AESEncrypt(str(level), key))
    # return utils.AESEncrypt(str(level), key)

@app.route('/genhashchain',methods=['POST','GET'])
def genhashchain():
	return utils.HashChainInit(request.form.get('username'))

if __name__ == '__main__':
    app.run(port=cm.PORT, debug=True)
