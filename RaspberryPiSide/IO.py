import numpy as np
import config
import serial
import time

# sp = config.port
if config.inputMode == 2:
    ser = serial.Serial(config.port, config.rate)

# directions
directions = ['N', 'E', 'S', 'W']

sData = ""

# get file editors
def outputFile(mode):
    return open(config.fpTXT + "outputDirections", str(mode), encoding='utf-8')
def inputFile(mode):
    return open(config.fpTXT + "generatedMaze", str(mode), encoding='utf-8')
def saveFile(mode):
    return open(config.fpTXT + "savedMaze", str(mode), encoding='utf-8')

# function to reroute setup based on input/output
def setupInput(mode):
    # manual or from file
    if mode == 1 or mode == 0:
        # clear output file
        outputFile("r+").truncate(0)
    # from file
    if mode == 1:
        setupInputFile()
    # serial
    if mode == 2:
        return setupSerial()

# function to reroute where input is coming from
def getData(mode, tile):
    if mode == 0:
        return getManualData(tile)
    if mode == 1:
        return getFileData(tile)
    if mode == 2:
        return requestData()

# receiving manual data from console
def getManualData(tile):
    walls = np.zeros(10, dtype=np.int8)
    inputStr = input("\tEnter MegaPi input data for Tile " + str(tile) + ": ")  # 1010 -> 1010100000
    for i in range(4):
        walls[i] = int(inputStr[i])
    walls[4] = 1
    for i in range(5, 10):
        walls[i] = 0
    return walls

# sets up file input, determines whether from generated or image
def setupInputFile():
    inputType = inputFile("r").readline()
    if inputType == "GENERATED\n":
        print("File input is a generated maze")
    elif inputType == "IMAGE\n":
        print("File input is a maze from image")
    else:
        raise ValueError("Invalid Input File Type!\nExpected: \"GENERATED\" or \"IMAGE\"\nGot: " + str(inputType))

# gets data from file depending whether from gen or input
def getFileData(tile):
    # skips until desired tile
    f = inputFile("r")
    for i in range(tile + 1):
        f.readline()
    return [int(j) for j in str(f.readline())[:10]]

# writes path to file
def sendFileData(pathLen):
    outputFile("a").write(sData[pathLen:] + "\n")
    outputFile("a").flush()

def writeMaze(file, header, maze, delete):
    if delete:
        file.truncate(0)
    if header:
        file.write(str(header) + "\n")
    for i in range(config.mazeSideLen ** 2):
        file.write(str(''.join(str(j) for j in maze[i])) + "\n")
    file.close()

def readMaze(file):
    maze = np.zeros((config.mazeSideLen ** 2, 10), dtype=np.int8)
    header = file.readline()
    for i in range(config.mazeSideLen ** 2):
        maze[i][:] = file.readline()
    file.close()
    return header[:len(header) - 1], maze

# sets up serial communication
def setupSerial():
    print("SETTING UP SERIAL")
    print("\tSerial setup on port: " + ser.name + "\n")
    print("waiting")

    while not ser.inWaiting():
        time.sleep(0.01)

    ser.read()  # do this to clean the buffer
    return config.port

# request and receive wall positions through serial
def requestData():
    send_message = 'g'
    ser.write(bytes(send_message.encode("ascii", "ignore")))
    walls = np.zeros(5)
    receive_message = ser.read()
    while receive_message.isdigit() is False:
        print("rms: " + str(receive_message))
        receive_message = ser.read()
    time.sleep(0.1)
    walls[3] = receive_message.decode("ascii", "ignore")
    receive_message = ser.read()
    time.sleep(0.1)
    walls[1] = receive_message.decode("ascii", "ignore")
    receive_message = ser.read()
    time.sleep(0.1)
    walls[0] = receive_message.decode("ascii", "ignore")
    return walls

def hasSerialMessage():
    return ser.in_waiting

# send path instructions through serial
def sendSerial(msg):
    if config.debug:
        print("Sending: " + msg)  # send msg over serial
    ser.write(bytes(msg.encode("ascii", "ignore")))
