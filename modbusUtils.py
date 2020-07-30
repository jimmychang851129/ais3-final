from typing import List, Callable, Any

def int2bytes(x: int, length=None) -> bytes:
    length = (x.bit_length() + 7) // 8 if length is None else length
    return x.to_bytes(length, 'big')

def bytes2int(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def compressBools(x: List[int]) -> bytes:
    return int2bytes(int(''.join(map(str, x[::-1])), 2), (len(x) + 7) // 8)[::-1]

def decompressBools(x: bytes) -> List[int]:
    return list(map(int, bin(bytes2int(x[::-1]))[2:]))[::-1]

def modbusSend(functionCode: int, dataRequest: bytes, send: Callable[[bytes], Any]) -> Any:
    # if not 1 <= functionCode <= 127:
    #     raise
    return send(assemblePDU(functionCode, dataRequests))

def assemblePDU(functionCode: int, dataRequest: bytes) -> bytes:
    # if not 1 <= functionCode <= 127:
    #     raise
    return int2bytes(functionCode) + dataRequest

def readCoils(startingAddress: int, quantityOfCoils : int) -> None:
    modbusSend(1, int2bytes(startingAddress) + int2bytes(quantityOfCoils))

def readDiscreteInputs(startingAddress: int, quantityOfInputs: int) -> None:
    modbusSend(2, int2bytes(startingAddress) + int2bytes(quantityOfInputs))

def readHoldingRegisters(startingAddress: int, quantityOfRegisters: int) -> None:
    modbusSend(3, int2bytes(startingAddress) + int2bytes(quantityOfRegisters))

def readInputRegisters(startingAddress: int, quantityOfInputRegisters: int) -> None:
    modbusSend(4, int2bytes(startingAddress) + int2bytes(quantityOfInputRegisters))

def writeSingleCoil(outputAddress: int, outputValue: int) -> None:
    modbusSend(5, int2bytes(outputAddress) + int2bytes(outputValue))

def writeSingleRegister(registerAddress: int, registerValue : int) -> None:
    modbusSend(6, int2bytes(registerAddress) + int2bytes(registerValue))

def writeMultipleCoils(startingAddress: int, outputValue: List[int]) -> None:
    quantityOfOutputs = len(outputValue)
    compressedOutputValue = compressBools(outputValue)
    modbusSend(15, int2bytes(startingAddress) + int2bytes(quantityOfOutputs) + int2bytes(len(compressedOutputValue)) + compressedOutputValue)

def writeMultipleRegisters(startingAddress: int, registersValue: List[int]) -> None:
    quantityOfRegisters = len(registerValue)
    modbusSend(16, int2bytes(startingAddress) + int2bytes(quantityOfRegisters) + int2bytes(quantityOfRegisters * 2) + b''.join(map(lambda x : x.to_bytes(2, 'big'), registersValue)))
