import socket,os
import Config as cm
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

#################################
# aes with GCM mod of operation #
#################################
# key: length 16
# IV: length 16
def AESEncrypt(data,key):
	try:
		nonceIV = os.urandom(16)
		obj = AES.new(key, AES.MODE_CBC, nonceIV)
		ct = obj.encrypt(data)
	except Exception as e:
		print("[utils.py error]AESEncrypt error")
		print(str(e))
		ct,nonceIV = "",0
	return ct,nonceIV

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
