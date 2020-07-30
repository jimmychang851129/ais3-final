from flask import Flask, render_template, flash, redirect, url_for
import os
from flask import request
import utils
import Config as cm

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/HMIquery', methods=['POST'])
def handleHMIRequest():
	level = request.form.get('HMIquery')
	key = "c"*16	# tmp
	return utils.AESEncrypt(str(level),key)

if __name__ == '__main__':
    app.run(port=cm.PORT, debug=True)
