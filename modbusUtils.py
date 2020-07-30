from typing import List
import socket

host = '127.0.0.1'
port = 4444

def int2bytes(x: int, length=None) -> bytes:
    length = (x.bit_length() + 7) // 8 if length is None else length
    return x.to_bytes(length, 'big')

def bytes2int(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def compressBools(x: List[int]) -> bytes:
    return int2bytes(int(''.join(map(str, x[::-1])), 2), (len(x) + 7) // 8)[::-1]

def decompressBools(x: bytes) -> List[int]:
    return list(map(int, bin(bytes2int(x[::-1]))[2:]))[::-1]

def modbusSend(functionCode: int, dataRequest: bytes) -> None:
    # if not 1 <= functionCode <= 127:
    #     raise
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        msg = assemblePDU(functionCode, dataRequest)
        print(msg)
        sock.sendall(msg)
        if msg[0] in [1, 2, 3, 4]:
            response = sock.recv(2)
            byteCount = response[1]
            response += sock.recv(byteCount)
        elif msg[0] in [5, 6, 15, 16]:
            response = sock.recv(5)
    print(response)

def assemblePDU(functionCode: int, dataRequest: bytes) -> bytes:
    # if not 1 <= functionCode <= 127:
    #     raise
    return int2bytes(functionCode) + dataRequest

def readCoils(startingAddress: int, quantityOfCoils : int) -> None:
    modbusSend(1, int2bytes(startingAddress, 2) + int2bytes(quantityOfCoils, 2))

def readDiscreteInputs(startingAddress: int, quantityOfInputs: int) -> None:
    modbusSend(2, int2bytes(startingAddress, 2) + int2bytes(quantityOfInputs, 2))

def readHoldingRegisters(startingAddress: int, quantityOfRegisters: int) -> None:
    modbusSend(3, int2bytes(startingAddress, 2) + int2bytes(quantityOfRegisters, 2))

def readInputRegisters(startingAddress: int, quantityOfInputRegisters: int) -> None:
    modbusSend(4, int2bytes(startingAddress, 2) + int2bytes(quantityOfInputRegisters, 2))

def writeSingleCoil(outputAddress: int, outputValue: int) -> None:
    modbusSend(5, int2bytes(outputAddress, 2) + int2bytes(outputValue, 2))

def writeSingleRegister(registerAddress: int, registerValue : int) -> None:
    modbusSend(6, int2bytes(registerAddress, 2) + int2bytes(registerValue, 2))

def writeMultipleCoils(startingAddress: int, outputValue: List[int]) -> None:
    quantityOfOutputs = len(outputValue)
    compressedOutputValue = compressBools(outputValue)
    modbusSend(15, int2bytes(startingAddress, 2) + int2bytes(quantityOfOutputs, 2) + int2bytes(len(compressedOutputValue)) + compressedOutputValue)

def writeMultipleRegisters(startingAddress: int, registersValue: List[int]) -> None:
    quantityOfRegisters = len(registersValue)
    modbusSend(16, int2bytes(startingAddress, 2) + int2bytes(quantityOfRegisters, 2) + int2bytes(quantityOfRegisters * 2) + b''.join(map(lambda x : x.to_bytes(2, 'big'), registersValue)))
