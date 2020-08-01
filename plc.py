#!/usr/bin/env python3

import modbusUtils
import asyncio
import Config

class PLC:
    def __init__(self, host, port, sensorProgram):
        self.host = host
        self.port = port
        self.sensorProgram = sensorProgram
        self.memory = [0 for i in range(524288)]
        self.PDUTranslationTable = {'coils' : 0,
                                    'discreteInput' : 65536,
                                    'inputRegisters' : 131072,
                                    'holdingRegisters' : 196608,}
        self.coilsAddressMap = dict(zip(range(1, 65537), range(0, 65536)))
        self.discreteInputAddressMap = dict(zip(range(100001, 165537), range(65536, 131072)))
        self.inputRegistersAddressMap = dict(zip(range(300001, 365537), range(131072, 196608)))
        self.holdingRegistersAddressMap = dict(zip(range(400001, 465537), range(196608, 262144)))
        self.modbusAddressMap = {**self.coilsAddressMap,
                                 **self.discreteInputAddressMap,
                                 **self.inputRegistersAddressMap,
                                 **self.holdingRegistersAddressMap,}

        self.functionDict = {1:  self.readCoils,
                             2:  self.readDiscreteInputs,
                             3:  self.readHoldingRegisters,
                             4:  self.readInputRegisters,
                             5:  self.writeSingleCoil,
                             6:  self.writeSingleRegister,
                             15: self.writeMultipleCoils,
                             16: self.writeMultipleRegisters,}

    async def handleConnection(self, reader, writer):
        try:
            while True:
                functionCode = await reader.read(1)
                retData = await self.functionDict.get(functionCode[0], lambda x : None)(reader)
                if retData:
                    writer.write(functionCode + retData)
                    await writer.drain()
        except:
            return

    async def listen(self):
        server = await asyncio.start_server(self.handleConnection, self.host, self.port)
        await server.serve_forever()

    async def listenSensor(self, sensor):
        while True:
            currentWaterLevel = int((await sensor.stdout.readline()).decode())
            self.memory[self.PDUTranslationTable['inputRegisters'] + Config.revmemLoc] = currentWaterLevel

    async def control(self):
        if isinstance(self.sensorProgram, str):
            sensor = await asyncio.create_subprocess_exec(self.sensorProgram, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        else:
            sensor = await asyncio.create_subprocess_exec(*self.sensorProgram, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        listenSensor = asyncio.create_task(self.listenSensor(sensor))

        lastTargetWaterLevel = self.memory[self.PDUTranslationTable['holdingRegisters'] + Config.memLoc]

        while True:
            targetWaterLevel = self.memory[self.PDUTranslationTable['holdingRegisters'] + Config.memLoc]
            if targetWaterLevel != lastTargetWaterLevel:
                sensor.stdin.write((str(targetWaterLevel) + '\n').encode())
                await sensor.stdin.drain()

                lastTargetWaterLevel = targetWaterLevel

            await asyncio.sleep(0.1)

    async def main(self):
        await asyncio.gather(self.listen(), self.control())

    def start(self):
        asyncio.run(self.main())

    async def readCoils(self, reader):
        startingAddress = modbusUtils.bytes2int(await reader.read(2))
        quantityOfCoils = modbusUtils.bytes2int(await reader.read(2))

        offset = self.PDUTranslationTable['coils']
        coilStatus = modbusUtils.compressBools(self.memory[offset + startingAddress:offset + startingAddress + quantityOfCoils])
        byteCount = len(coilStatus)
        return modbusUtils.int2bytes(byteCount) + coilStatus

    async def readDiscreteInputs(self, reader):
        startingAddress = modbusUtils.bytes2int(await reader.read(2))
        quantityOfInputs = modbusUtils.bytes2int(await reader.read(2))

        offset = self.PDUTranslationTable['discreteInput']
        inputStatus = modbusUtils.compressBools(self.memory[offset + startingAddress:offset + startingAddress + quantityOfInputs])
        byteCount = len(inputStatus)
        return modbusUtils.int2bytes(byteCount) + inputStatus

    async def readHoldingRegisters(self, reader):
        startingAddress = modbusUtils.bytes2int(await reader.read(2))
        quantityOfRegisters = modbusUtils.bytes2int(await reader.read(2))

        offset = self.PDUTranslationTable['holdingRegisters']
        registerValue = b''.join(map(lambda x : x.to_bytes(2, 'big'), self.memory[offset + startingAddress:offset + startingAddress + quantityOfRegisters]))
        byteCount = len(registerValue)
        return modbusUtils.int2bytes(byteCount) + registerValue

    async def readInputRegisters(self, reader):
        startingAddress = modbusUtils.bytes2int(await reader.read(2))
        quantityOfInputRegisters = modbusUtils.bytes2int(await reader.read(2))

        offset = self.PDUTranslationTable['inputRegisters']
        inputRegisters = b''.join(map(lambda x : x.to_bytes(2, 'big'), self.memory[offset + startingAddress:offset + startingAddress + quantityOfInputRegisters]))
        byteCount = len(inputRegisters)
        return modbusUtils.int2bytes(byteCount) + inputRegisters

    async def writeSingleCoil(self, reader):
        data = await reader.read(4)
        outputAddress = modbusUtils.bytes2int(data[0:2])
        outputValue = modbusUtils.bytes2int(data[2:4])

        offset = self.PDUTranslationTable['coils']
        if outputValue == 0x0000:
            self.memory[offset + outputAddress] = 0
        elif outputValue == 0xFF00:
            self.memory[offset + outputAddress] = 1

        return data

    async def writeSingleRegister(self, reader):
        data = await reader.read(4)
        registerAddress = modbusUtils.bytes2int(data[0:2])
        registerValue = modbusUtils.bytes2int(data[2:4])

        offset = self.PDUTranslationTable['holdingRegisters']
        self.memory[offset + registerAddress] = registerValue

        return data

    async def writeMultipleCoils(self, reader):
        data = await reader.read(5)
        startingAddress = modbusUtils.bytes2int(data[0:2])
        quantityOfOutputs = modbusUtils.bytes2int(data[2:4])
        byteCount = modbusUtils.bytes2int(data[4:5])
        outputValue = modbusUtils.zeroPadOrTruncate(modbusUtils.decompressBools(await reader.read(byteCount)), quantityOfOutputs)

        offset = self.PDUTranslationTable['coils']
        self.memory[offset + startingAddress:offset + startingAddress + quantityOfOutputs] = outputValue

        return data[0:4]

    async def writeMultipleRegisters(self, reader):
        data = await reader.read(5)
        startingAddress = modbusUtils.bytes2int(data[0:2])
        quantityOfRegisters = modbusUtils.bytes2int(data[2:4])
        byteCount = modbusUtils.bytes2int(data[4:5])
        registersValue = await reader.read(byteCount)
        registersValue = list(map(modbusUtils.bytes2int, modbusUtils.splitIntoChunks(registersValue, 2)))

        offset = self.PDUTranslationTable['holdingRegisters']
        self.memory[offset + startingAddress:offset + startingAddress + quantityOfRegisters] = registersValue

        return data[0:4]

if __name__ == '__main__':
    plc = PLC('127.0.0.1', 4444, ['python3', 'Sensor2.py'])
    plc.start()
