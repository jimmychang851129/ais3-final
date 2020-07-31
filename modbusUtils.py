from typing import List, Tuple, Any, Optional
import socket

'''
Bytes Processing Utilities
'''

def int2bytes(x: int, length=None) -> bytes:
    length = (x.bit_length() + 7) // 8 if length is None else length
    return x.to_bytes(length, 'big')

def bytes2int(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def compressBools(x: List[int]) -> bytes:
    return int2bytes(int(''.join(map(str, x[::-1])), 2), (len(x) + 7) // 8)[::-1]

def decompressBools(x: bytes) -> List[int]:
    return list(map(int, bin(bytes2int(x[::-1]))[2:]))[::-1]

def zeroPadOrTruncate(sequence, targetLen):
    return sequence[:targetLen] + [0] * (targetLen - len(sequence))

def splitIntoChunks(sequence, chunkSize):
    return (sequence[i:i + chunkSize] for i in range(0, len(sequence), chunkSize))

'''
Modbus Functions
'''

def modbusSetup(host: str, port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def modbusClose(sock: socket.socket) -> None:
    sock.close()

def modbusSend(sock: socket.socket, functionCode: int, dataRequest: bytes) -> None:
    sock.sendall(assemblePDU(functionCode, dataRequest))

def modbusRecv(sock: socket.socket) -> bytes:
    functionCode = sock.recv(1)
    if functionCode[0] in [1, 2, 3, 4]:
        byteCount = sock.recv(1)
        response = byteCount + sock.recv(byteCount[0])
    elif functionCode[0] in [5, 6, 15, 16]:
        response = sock.recv(4)
    return functionCode + response

def assemblePDU(functionCode: int, dataRequest: bytes) -> bytes:
    return int2bytes(functionCode) + dataRequest

'''
Modbus Commands
'''

def readCoils(sock: socket.socket, startingAddress: int, quantityOfCoils : int) -> None:
    modbusSend(sock, 1, int2bytes(startingAddress, 2) + int2bytes(quantityOfCoils, 2))

def readDiscreteInputs(sock: socket.socket, startingAddress: int, quantityOfInputs: int) -> None:
    modbusSend(sock, 2, int2bytes(startingAddress, 2) + int2bytes(quantityOfInputs, 2))

def readHoldingRegisters(sock: socket.socket, startingAddress: int, quantityOfRegisters: int) -> None:
    modbusSend(sock, 3, int2bytes(startingAddress, 2) + int2bytes(quantityOfRegisters, 2))

def readInputRegisters(sock: socket.socket, startingAddress: int, quantityOfInputRegisters: int) -> None:
    modbusSend(sock, 4, int2bytes(startingAddress, 2) + int2bytes(quantityOfInputRegisters, 2))

def writeSingleCoil(sock: socket.socket, outputAddress: int, outputValue: int) -> None:
    outputValue = 0xFF00 if outputValue else 0x0000
    modbusSend(sock, 5, int2bytes(outputAddress, 2) + int2bytes(outputValue, 2))

def writeSingleRegister(sock: socket.socket, registerAddress: int, registerValue : int) -> None:
    modbusSend(sock, 6, int2bytes(registerAddress, 2) + int2bytes(registerValue, 2))

def writeMultipleCoils(sock: socket.socket, startingAddress: int, outputValue: List[int]) -> None:
    quantityOfOutputs = len(outputValue)
    compressedOutputValue = compressBools(outputValue)
    modbusSend(sock, 15, int2bytes(startingAddress, 2) + int2bytes(quantityOfOutputs, 2) + int2bytes(len(compressedOutputValue)) + compressedOutputValue)

def writeMultipleRegisters(sock: socket.socket, startingAddress: int, registersValue: List[int]) -> None:
    quantityOfRegisters = len(registersValue)
    modbusSend(sock, 16, int2bytes(startingAddress, 2) + int2bytes(quantityOfRegisters, 2) + int2bytes(quantityOfRegisters * 2) + b''.join(map(lambda x : x.to_bytes(2, 'big'), registersValue)))

'''
Modbus Response Parsing Functions
'''

def parseReadCoilsResponse(response: bytes, expectedLen: Optional[int] = None) -> List[int]:
    readBytes = decompressBools(response[2:])
    if expectedLen is not None:
        readBytes = zeroPadOrTruncate(readBytes, expectedLen)
    return readBytes

def parseReadDiscreteInputsResponse(response: bytes, expectedLen: Optional[int] = None) -> List[int]:
    readBytes = decompressBools(response[2:])
    if expectedLen is not None:
        readBytes = zeroPadOrTruncate(readBytes, expectedLen)
    return readBytes

def parseReadHoldingRegistersResponse(response: bytes) -> List[int]:
    readBytes = response[2:]
    return list(map(bytes2int, splitIntoChunks(readBytes, 2)))

def parseReadInputRegistersResponse(response: bytes) -> List[int]:
    readBytes = response[2:]
    return list(map(bytes2int, splitIntoChunks(readBytes, 2)))

def parseWriteSingleCoilResponse(response: bytes) -> Tuple[int, int]:
    return (bytes2int(response[1:3]), bytes2int(response[3:5]))

def parseWriteSingleRegisterResponse(response: bytes) -> Tuple[int, int]:
    return (bytes2int(response[1:3]), bytes2int(response[3:5]))

def parseWriteMultipleCoilsResponse(response: bytes) -> Tuple[int, int]:
    return (bytes2int(response[1:3]), bytes2int(response[3:5]))

def parseWriteMultipleRegistersResponse(response: bytes) -> Tuple[int, int]:
    return (bytes2int(response[1:3]), bytes2int(response[3:5]))
