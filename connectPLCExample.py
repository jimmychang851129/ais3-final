import asyncio
import modbusUtils

sock = modbusUtils.modbusSetup('127.0.0.1', 4444)

while True:
    cmd = list(map(int, input().split()))
    if len(cmd) == 0:
        continue
    code = cmd[0]
    if code == 1:
        startingAddress = cmd[1]
        quantity = cmd[2]
        modbusUtils.modbusSend(sock, modbusUtils.makeReadCoilsRequest(startingAddress, quantity))

        response = modbusUtils.parseReadCoilsResponse(modbusUtils.modbusRecv(sock), quantity)
        print(response)
    elif code == 2:
        startingAddress = cmd[1]
        quantity = cmd[2]
        modbusUtils.modbusSend(sock, modbusUtils.makeReadDiscreteInputsRequest(startingAddress, quantity))

        response = modbusUtils.parseReadDiscreteInputsResponse(modbusUtils.modbusRecv(sock), quantity)
        print(response)
    elif code == 3:
        startingAddress = cmd[1]
        quantity = cmd[2]
        modbusUtils.modbusSend(sock, modbusUtils.makeReadHoldingRegistersRequest(startingAddress, quantity))

        response = modbusUtils.parseReadHoldingRegistersResponse(modbusUtils.modbusRecv(sock))
        print(response)
    elif code == 4:
        startingAddress = cmd[1]
        quantity = cmd[2]
        modbusUtils.modbusSend(sock, modbusUtils.makeReadInputRegistersRequest(startingAddress, quantity))

        response = modbusUtils.parseReadInputRegistersResponse(modbusUtils.modbusRecv(sock))
        print(response)
    elif code == 5:
        address = cmd[1]
        value = cmd[2]
        modbusUtils.modbusSend(sock, modbusUtils.makeWriteSingleCoilRequest(address, value))

        response = modbusUtils.parseWriteSingleCoilResponse(modbusUtils.modbusRecv(sock))
        print(response)
    elif code == 6:
        address = cmd[1]
        value = cmd[2]
        modbusUtils.modbusSend(sock, modbusUtils.makeWriteSingleRegisterRequest(address, value))

        response = modbusUtils.parseWriteSingleRegisterResponse(modbusUtils.modbusRecv(sock))
        print(response)
    elif code == 15:
        startingAddress = cmd[1]
        valueList = cmd[2:]
        modbusUtils.modbusSend(sock, modbusUtils.makeWriteMultipleCoilsRequest(startingAddress, valueList))

        response = modbusUtils.parseWriteMultipleCoilsResponse(modbusUtils.modbusRecv(sock))
        print(response)
    elif code == 16:
        startingAddress = cmd[1]
        valueList = cmd[2:]
        modbusUtils.modbusSend(sock, modbusUtils.makeWriteMultipleRegistersRequest(startingAddress, valueList))

        response = modbusUtils.parseWriteMultipleRegistersResponse(modbusUtils.modbusRecv(sock))
        print(response)
    elif code == 88:
        break

modbusUtils.modbusClose(sock)
