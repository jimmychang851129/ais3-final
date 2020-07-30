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
	return json.dumps(result)

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

def HashChainInit():
	key = os.urandom(cm.hashkeyLength)
	l = []
	hashf = SHA256.new()
	for i in range(cm.hashchainLength):
		hashf.update(key)
		l.append(hashf.hexdigest())
	return ','.join([x for x in l])
