import os

Basedir = ""
AESKeyLength = 128
logfile = os.path.join(Basedir,"log.txt")
hashchainLength = 100
PORT = 5000

jwtFormat = {
	"username":"",
	"hashchainVal":"",
	"cntDay":0,
}