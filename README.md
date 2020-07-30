# ais3-final

## Problem definition

Modbus is vulnerable to response injection, command injection, recon due to its unauthenticated transmission.

For example, an attacker can easily retrieve all possible information of the OT environment such as machine status from HMI. Furthermore, attacker can conduct response injection or command injection if either the HMI or device is compromised.

## Solution

### Assumption

1. one-wayness and weak collision resistence of cryptographic hash function
2. the origin key of hashchain is randomly generated and not known to anyone

### Details

Authentication layer(Auth) between PLC and HMI

- AES encryption on PLC response based on key in hash chain

## Difficulties

1. User authentication
2. hash chain storage

## Environment

python3.6

## Execution

```
$ pip install -r requirements.txt
$ python3 app.py
```
occupy port: 5000

## Spec

### HMI

- index.html
	- selection: 
		- Increase, Decrease, Report Water level, Report SystemInfo
	- jwt token generate button
	- Input:
		- input water level
		- input userkey
	- output:
		- output block(system Info)
- function
	- AES encryption/decryption(brix/CryptoJS)

### Auth

- AES encrypt/decrypt
- jwt token, hashchain generation
- jwt token, hashchain validation
- command whitelist

### PLC

- modbusutil.py implementation
	- implement request, response function, and webserver along with sensor can import these function

### sensor

- api
	- water level report
	- Increase water level
	- Decrease water level
	- System Info report

### Conenction spec

#### Web & Auth

```
Command: web -> Auth
{
	Request: /HMIquery
	command: increase/decrease/report...
	jwt token: .....
}

Command Response: Auth -> Web
{
	msg: encrypted msg,IV
}

Generate HashChain: Web -> Auth
{
	Request: /genhashchain
	Simply a requests
}

Return HashChain: Auth -> Web
{
	return hash chain in string format
}

```

## links

[hackmd notes](https://hackmd.io/d_7YG7d2Tl6sjiXiLwNESQ)
[ppt]
