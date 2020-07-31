from flask import Flask, render_template, flash, redirect, url_for, jsonify
import os
from flask import request
import utils, modbusUtils
import Config as cm

app = Flask(__name__)

sock = modbusUtils.modbusSetup(cm.host,cm.PLCport)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/HMIquery',methods=['POST','GET'])
def handleHMIRequest():
	waterlevel = int(request.form.get('jwttoken'))
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
	else:
		modbusUtils.modbusSend(sock, modbusUtils.makeWriteSingleRegisterRequest(cm.memLoc, waterlevel))
		response = modbusUtils.parseWriteSingleRegisterResponse(modbusUtils.modbusRecv(sock))
		# modbusUtils.modbusSend(sock, modbusUtils.makeReadInputRegistersRequest(cm.revmemLoc, 1))
		# response = modbusUtils.parseReadInputRegistersResponse(modbusUtils.modbusRecv(sock))
	return jsonify(utils.AESEncrypt(str(waterlevel), key))

@app.route('/genhashchain',methods=['POST','GET'])
def genhashchain():
	return utils.HashChainInit(request.form.get('username'))

if __name__ == '__main__':
    app.run(port=cm.PORT, debug=True)
