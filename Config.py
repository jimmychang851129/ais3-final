import os

Basedir = ""
AESKeyLength = 128
logfile = os.path.join(Basedir,"log.txt")
keychainfile = os.path.join(Basedir,"keychain.txt")
hashchainLength = 5
hashkeyLength = 10
PORT = 5000

staffjwtFormat = {
	"username":"",
	"supersecretKey":"",
	"cntDay":0,
}

AuthjwtFormat = {
	"username":"",
	"hashChainVal":"",
}