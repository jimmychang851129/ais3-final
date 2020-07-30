# ais3-final

## Problem definition

Modbus is vulnerable to response injection, command injection, recon due to its unauthenticated transmission.

For example, an attacker can easily retrieve all possible information of the OT environment such as machine status from HMI. Furthermore, attacker can conduct response injection or command injection if either the HMI or device is compromised.

## Solution

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

## links

[hackmd notes](https://hackmd.io/d_7YG7d2Tl6sjiXiLwNESQ)
[ppt]
