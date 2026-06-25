
from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import ForceSensor, Motor
from pybricks.tools import wait

# Rádió
hub = PrimeHub(broadcast_channel=1)

# TREE
tree_button = ForceSensor(Port.A)
tree_selector = Motor(Port.B, Direction.CLOCKWISE)

# SIGN
sign_button = ForceSensor(Port.E)
sign_selector = Motor(Port.C, Direction.CLOCKWISE)

# ROCK
rock_button = ForceSensor(Port.F)
rock_selector = Motor(Port.D, Direction.CLOCKWISE)

counter = 0

tree_was_pressed = False
sign_was_pressed = False
rock_was_pressed = False

# Selector motorok nullázása
#selector_motor.reset_angle(0) #inkább ne mert ha el van tekergetve amikor rátöltjük akkor megszívjuk
#tree_selector.reset_angle(0)
#sign_selector.reset_angle(0)
#rock_selector.reset_angle(0)

def get_command(robot_id, selector_motor):
    angle = selector_motor.angle() % 360

    if angle < 45 or angle >= 315:
        return "HOME"
    elif angle < 135:
        if robot_id == "TREE":
            return "RED"
        else:           # ROCK és SIGN
            return "BLUE"        
    elif angle < 225:
        return "GREEN"
    else:
        if robot_id == "TREE":
            return "BLUE"
        else:           # ROCK és SIGN
            return "RED"

def send_command(robot_id, selector_motor):
    global counter

    counter += 1
    command = get_command(robot_id, selector_motor)
    message = (robot_id, command, counter)

    hub.ble.broadcast(message)
    print("sent:", message)

while True:
    tree_pressed = tree_button.force() >= 0.1
    sign_pressed = sign_button.force() >= 0.1
    rock_pressed = rock_button.force() >= 0.1

    if tree_pressed and not tree_was_pressed:
        send_command("TREE", tree_selector)

    if sign_pressed and not sign_was_pressed:
        send_command("SIGN", sign_selector)

    if rock_pressed and not rock_was_pressed:
        send_command("ROCK", rock_selector)

    tree_was_pressed = tree_pressed
    sign_was_pressed = sign_pressed
    rock_was_pressed = rock_pressed

    wait(50)
