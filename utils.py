import socket,os
import Config as cm
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
import math, json, datetime

############
# hmac sig #
############
def hmacSig(key,msg):
	h = HMAC.new(key)	#signature
	h.update(msg.encode())
	return h.hexdigest()

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

def writeToken(user,token):
	with open(user+".json",'w') as fw:
		json.dump(token,fw)

def ReadToken(user):
	output = 0
	with open(user+".json",'r') as f:
		output = json.load(f)
	return output
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
	writeToken(username,jwtToken)
	return jwtToken

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
	return text+','+hmacSig(key,text)

#######################
# user authentication #
#######################
# return 0 if false 1 if true
def authcheck(plaintext,sig,waterlevel):
	print("ininin")
	user,timestamp = plaintext[:plaintext.index('2')],plaintext[plaintext.index('2'):]
	hashchainValue = 0
	with open(cm.keychainfile,'r') as f:
		for line in f:
			if user in line:
				hashchainValue = line.strip().split(',')[-1]	# only retrieve the last value in hashchain
	if hashchainValue == 0:	# jwttoken error username not found
		print("[utils.py]authcheck error, jwttoken user not found")
		return 0
	msgtext = user + datetime.datetime.now().strftime('%Y-%m-%d-%H')
	sigcheck = hmacSig(hashchainValue.encode(),msgtext)
	print("sig = ",sigcheck,sig)
	if sigcheck == sig:
		print("Authentication sucess")
		writelog("Authentication sucess")
		writelog("%s\thashchainkey = %s\n"%(user,hashchainValue))
		DeleteKey(user)
		data = ReadToken(user)
		data['cntDay'] += 1
		writeToken(user,data)
		return 1
	print("Authentication failed")
	print("%s -> %s"%(sigcheck,sig))
	return 0

###################
# keychain delete #
###################
def DeleteKey(user):
	l = []
	with open(cm.keychainfile,'r') as f:
		for line in f:
			if user not in line.split(',')[0]:
				l.append(line.strip())
			else:
				l.append(','.join([x for x in line.split(',')[:-1]]))
				writelog("Delete user %s key %s"%(user,line.split(',')[-1]))
	with open(cm.keychainfile,'w') as fw:
		for ele in l:
			fw.write(ele+"\n")