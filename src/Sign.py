from pybricks.hubs import PrimeHub, ThisHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

#hub = PrimeHub()

# Setup
hub = PrimeHub(observe_channels=[1])

left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)   # A hátrafelé forogjon
right_motor = Motor(Port.D, Direction.CLOCKWISE)         # B előrefelé forogjon

robot = DriveBase(
    left_motor,
    right_motor,
    wheel_diameter=31,
    axle_track=85
)
color_sensor = ColorSensor(Port.B)
ROBOT_ID = "SIGN"
last_counter = 0

robot.settings(straight_speed=100,turn_rate=100)

def falhoz_igazodik_elol():
    robot.use_gyro(False)
    robot.straight(100)
    robot.use_gyro(True)

def falhoz_igazodik_hatul():
    robot.use_gyro(False)
    robot.straight(-100)
    robot.use_gyro(True)

def menj_feketeig():
    robot.drive(100,0)
    while color_sensor.color() != Color.NONE:
        wait(10)
    robot.stop()

def menj_pirosig():
    robot.drive(100,0)
    while color_sensor.color() != Color.RED:
        wait(10)
    robot.stop()

def menj_zoldig():
    robot.drive(100,0)
    while color_sensor.color() != Color.GREEN:
        wait(10)
    robot.stop() 
       
def menj_kekig():
    robot.drive(100,0)
    while color_sensor.color() != Color.BLUE:
        wait(10)
    robot.stop()    
def szin_detektalo():
    while True:
        print(color_sensor.color())
        wait(100)

status = "PARKING"
def round1():
    global status
    robot.straight(40)
    #robot.straight(-10)
    robot.turn(-89)
    menj_feketeig()
    robot.straight(15)
    menj_feketeig()
    robot.straight(15)
    menj_feketeig()
    robot.straight(15)
    menj_feketeig()
    robot.straight(80)
    robot.turn(89)
    falhoz_igazodik_hatul()
    robot.straight(300)
    falhoz_igazodik_elol()
    robot.straight(-20)
    robot.turn(91)
    menj_zoldig()
    robot.straight(140)
    robot.turn(89)
    falhoz_igazodik_hatul()
    robot.straight(300)
    falhoz_igazodik_elol()
    robot.straight(-40)
    robot.turn(89)
    menj_feketeig()
    robot.straight(-10)
    robot.turn(90)
    falhoz_igazodik_hatul()
    status = "PARKING"


def menjhaza():
    global status
    if status != "PARKING" :
        menj_zoldig()
        robot.straight(140)
        robot.turn(89)
        falhoz_igazodik_hatul()
        robot.straight(300)
        falhoz_igazodik_elol()
        robot.straight(-40)
        robot.turn(89)
        menj_feketeig()
        robot.straight(-10)
        robot.turn(90)
        falhoz_igazodik_hatul()
        status = "PARKING"

def korpirosig():
    global status
    if status == "PARKING":
        robot.straight(40)
        #robot.straight(-10)
        robot.turn(-89)
        menj_feketeig()
        robot.straight(15)
        menj_feketeig()
        robot.straight(15)
        menj_feketeig()
        robot.straight(15)
        menj_feketeig()
        robot.straight(80)
        robot.turn(89)
        falhoz_igazodik_hatul()
        robot.straight(300)
        falhoz_igazodik_elol()
        robot.straight(-20)
        robot.turn(91)
        menj_pirosig()
        status = "PIROS"
    elif status == "ZOLD":
        menjhaza()
        korpirosig()
    else:
        menj_pirosig()
        status = "PIROS"

def korzoldig():
    global status
    if status == "PARKING":  
        robot.straight(40)
        #robot.straight(-10)
        robot.turn(-89)
        menj_feketeig()
        robot.straight(15)
        menj_feketeig()
        robot.straight(15)
        menj_feketeig()
        robot.straight(15)
        menj_feketeig()
        robot.straight(80)
        robot.turn(89)
        falhoz_igazodik_hatul()
        robot.straight(300)
        falhoz_igazodik_elol()
        robot.straight(-20)
        robot.turn(91)
        menj_zoldig()
        status = "ZOLD"
    else:
        menj_zoldig()
        status = "ZOLD"

def korkekig():
    global status
    if status == "PARKING":
        robot.straight(40)
        #robot.straight(-10)
        robot.turn(-89)
        menj_feketeig()
        robot.straight(15)
        menj_feketeig()
        robot.straight(15)
        menj_feketeig()
        robot.straight(15)
        menj_feketeig()
        robot.straight(80)
        robot.turn(89)
        falhoz_igazodik_hatul()
        robot.straight(300)
        falhoz_igazodik_elol()
        robot.straight(-20)
        robot.turn(91)
        menj_kekig()
        status = "KEK"
    else:
        menjhaza()
        korkekig()

while True:
    msg = hub.ble.observe(1)

    if msg is not None:
        robot_id, command, counter = msg
        print("received:", msg)
        if robot_id == ROBOT_ID and counter != last_counter:
            last_counter = counter
            print("received:", msg)

            if command == "HOME":
                #robot.turn(-90)      # balra 90 fok
                menjhaza()
            elif command == "RED":
                #robot.straight(200)  # előre 20 cm
                korpirosig()
            elif command == "BLUE":
                #robot.straight(-200) # hátra 20 cm
                korkekig()
            elif command == "GREEN":
                #robot.turn(90)       # jobbra 90 fok
                korzoldig()
        if robot_id == 'ALL' and counter != last_counter:
            last_counter = counter
            if command == "RED":
                round1() #egyedül 1 kör
            elif command == "GREEN": 
                #mindannyian mennek
                wait(12000) #mindannyian mennek, ő a negyedik ezért 4x3 másodpercet vár
                round1()
            elif command == "BLUE":
                #mindannyian 3 kör
                wait(12000)
                for i in range(3):
                    round1()
            else:
                robot.turn(360)
    wait(50)
