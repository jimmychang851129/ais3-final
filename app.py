from flask import Flask, render_template, flash, redirect, url_for,
import os
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/HMIquery',methods=['POST'])
def handleHMIRequest():
	level = request.form.get('HMIquery')
	print("level = ",level)


if __name__ == '__main__':
    app.debug = True
    app.run()