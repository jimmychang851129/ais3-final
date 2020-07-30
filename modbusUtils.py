from typing import List, Callable, Any

def int2bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def bytes2int(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

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

def writeMultipleCoils(startingAddress: int, quantityOfOutputs: int, byteCount: int, outputValue: List[int]) -> None:
    modbusSend(15, int2bytes(startingAddress) + int2bytes(quantityOfOutputs) + int2bytes(byteCount) + b''.join(map(int2bytes, outputValue)))

def writeMultipleRegisters(startingAddress: int, quantityOfRegisters: int, byteCount: int, registersValue: List[int]) -> None:
    modbusSend(16, int2bytes(startingAddress) + int2bytes(quantityOfRegisters) + int2bytes(byteCount) + b''.join(map(int2bytes, registersValue)))
