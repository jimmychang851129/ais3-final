import socket,os
import Config as cm
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import math,json

#################################
# aes with GCM mod of operation #
#################################
# key: length 16
# IV: length 16
# data: pad to 16
def AESEncrypt(data,key):
	result = {
		"cipher":"",
		"IV":0
	}
	try:
		key = key.encode()
		data = data.encode() + b'\0'*(math.ceil(len(data)/16)*16 - len(data))
		nonceIV = os.urandom(16)
		result['IV'] = nonceIV.hex()
		obj = AES.new(key, AES.MODE_CBC, nonceIV)
		result['cipher'] = obj.encrypt(data).hex()
	except Exception as e:
		print("[utils.py error]AESEncrypt error")
		print(str(e))
	return result

def AESDecrypt(cipher,key,IV):
	try:
		obj = AES.new(key, AES.MODE_CBC, IV)
		plain = obj.decrypt(cipher)
	except Exception as e:
		print("[utils.py error]AESDecrypt error")
		print(str(e))
		plain = ""
	return plain

def writelog(data):
	with open(cm.logfile,'w') as fw:
		if type(data) is list:
			for ele in data:
				fw.write(str(ele)+"\n")
		else:
			fw.write(data+"\n")

#####################
# register new user #
#####################
# for demonstration, we implement it online
def HashChainInit(username):
	key = os.urandom(cm.hashkeyLength)
	l = []
	jwtToken = dict(cm.staffjwtFormat)
	jwtToken['username'] = username
	jwtToken['supersecretKey'] = key.hex()
	hashf = SHA256.new()
	for i in range(cm.hashchainLength):
		hashf.update(key)
		l.append(hashf.hexdigest())
	result = ','.join([x for x in l])
	with open(cm.keychainfile,'a+') as fw:
		fw.write(username+','+result+"\n")
	return jwtToken