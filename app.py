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
	waterlevel = request.form.get('jwttoken')
	plaintext,sig = request.form.get('HMIquery').split(',')
	print("request = ",plaintext,sig,waterlevel)
	key = "c"*16	# tmp
	res = {
		"errmsg":"",
		"data":"123"
	}
	if utils.authcheck(plaintext,sig,waterlevel) == 0:
		res['errmsg'] = "Authentication failed"
		return res
	return jsonify(utils.AESEncrypt(str(waterlevel), key))

@app.route('/genhashchain',methods=['POST','GET'])
def genhashchain():
	return utils.HashChainInit(request.form.get('username'))

if __name__ == '__main__':
    app.run(port=cm.PORT, debug=True)
