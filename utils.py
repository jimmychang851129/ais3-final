import socket,os
import Config as cm
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
import math, json, datetime

#################################
# aes with CBC mod of operation #
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
		key = key.encode()
		cipher = bytes.fromhex(cipher)
		obj = AES.new(key, AES.MODE_CBC,  bytes.fromhex(IV))
		plain = obj.decrypt(cipher)
	except Exception as e:
		print("[utils.py error]AESDecrypt error")
		print(str(e))
		plain = ""
	return plain

def writelog(data):
	with open(cm.logfile,'a+') as fw:
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
	key = os.urandom(cm.hashkeyLength).hex()
	l = []
	jwtToken = dict(cm.staffjwtFormat)
	jwtToken['username'] = username
	jwtToken['supersecretKey'] = key
	for i in range(cm.hashchainLength):
		hashf = SHA256.new()
		hashf.update(key.encode())
		l.append(hashf.hexdigest())
		key = hashf.hexdigest()
	result = ','.join([x for x in l])
	with open(cm.keychainfile,'a+') as fw:
		fw.write(username+','+result+"\n")
	writelog("%s register success"%(username))
	writelog("jwt token: %s"%(json.dumps(jwtToken)))
	sig = JWTToHmac(jwtToken)
	jwtToken['sig'] = sig
	print("jwtToken = ",jwtToken)
	return jwtToken

#######################
# user authentication #
#######################
# need modify(hmac validation)
# given jwt token, validate if it contains correct hash chain value
# return 0 if false 1 if true
def HashChainValidation(jwttoken):
	hashchainValue = 0
	with open(keychainfile,'r') as f:
		for line in f:
			if jwtToken['username'] in line:
				hashchainValue = line.strip().split(',')[-1]	# only retrieve the last value in hashchain
	if hashchainValue == 0:	# jwttoken error username not found
		print("[utils.py]HashChainValidation error, jwttoken user not found")
		return 0
	if jwttoken['hashChainVal'] == hashchainValue:
		return 1
	print("[utils.py]HashChainValidation error, jwttoken hashchain value error")
	print("%s -> %s"%(jwttoken['hashChainVal'],hashchainValue))
	return 0

####################
# staffjwt to hmac #
####################
# should also be done in a offline device
# for demonstration, implement it as a function here
# input staffJWT(output of HashChainInit), return Hmac of the hash chain
# hmac(hashchainkey, username+2020-07-31-14)
def JWTToHmac(staffjwt):
	try:
		key = staffjwt['supersecretKey'].encode()
	except Exception as e:
		print("[utils.py]key encode error")
		print(str(e))
	for i in range(cm.hashchainLength - staffjwt['cntDay']):
		hashf = SHA256.new()
		hashf.update(key)
		key = hashf.hexdigest().encode()
	print("final key = ",key)
	text = staffjwt['username'] + datetime.datetime.now().strftime('%Y-%m-%d-%H')
	h = HMAC.new(key)	#signature
	h.update(text.encode())
	return text+','+h.hexdigest()
