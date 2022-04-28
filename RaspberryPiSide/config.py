# config file, because some settings might differ while debugging, or on different systems

mazeSideLen = 10  # must be even
floorCount = 3  # starts at middle floor
inputMode = 1  # 0 -> manual, 1 -> input or gen from file, 2 -> serial
recursionLimit = (mazeSideLen ** 2) * floorCount  # buffer added on setup

wallPercentage = 50  # percentage of tiles that should be walls for random generation of maze
blackTilePercentage = 5  # percent of black tiles when randomly generating a maze
silverTilePercentage = 2  # percent of silver tiles when randomly generating a maze
genFromImage = False  # if false, will generate random maze
redoLastMaze = False  # this setting allows you to rerun the last maze, maybe if a bug or problem occurred in it

showDisplay = True  # 0 no display, 1 is display
displayRate = 1  # in milliseconds, 0 for until keypress
displaySize = 500  # display size, range from (0 - 1000), see line below
displaySize = displaySize // mazeSideLen  # adjust for equal image size

importantDebug = True  # important print statements, overrides other settings
BFSDebug = True  # print statements for maze traversal
victimDebug = False  # shows camera feeds
saveVictimDebug = False  # saves victim images if found
serialDebug = True  # prints serial IO

port = "/dev/ttyS0"  # serial port path (serial: /dev/ttyAMA0)
rate = 9600  # serial port rate

doVictim = True  # check for color and letter victims
cameraCount = 2  # number of cameras, cam0 is left, cam1 is right. if only one camera, left
cameraWidth = 160  # width of camera feed for both cameras
cameraHeight = 128  # height of camera feed for both cameras

manualCheckpointLoading = False  # load back to last checkpoint when 'c' is pressed

# serial messages in order for:
# forward, left, right, back, EOI, (end of single instruction), SOD (start of dir.), EOD (end of directions)
# example: if ["a", "b", "c", "d", ".", "$", "%"], directions for forward, left, left, forward would be:
# $a.b.b.a.% and will be sent as "$", "a.", "b." etc.      ALL MESSAGES MUST BE ONE CHAR
serialMessages = ["F", "L", "R", "B", "U", "D", ";", "{", "}"]

# fp -> file path
fpALL = "../RaspberryPiSide/"
fpKNN = fpALL + "KNN/"
fpTXT = fpALL + "IOFiles/"
fpIMG = fpALL + "IOFiles/"
fpVIC = fpALL + "IOFiles/victimImages/"
