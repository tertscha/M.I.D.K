from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import ForceSensor, Motor
from pybricks.tools import wait

# ---------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------

hub = PrimeHub(broadcast_channel=1)

# HOUSE
house_button = ForceSensor(Port.E)
house_selector = Motor(Port.C, Direction.CLOCKWISE)

# ALL
all_button = ForceSensor(Port.F)
all_selector = Motor(Port.B, Direction.CLOCKWISE)

counter = 0

house_was_pressed = False
all_was_pressed = False

#house_selector.reset_angle(0)
#all_selector.reset_angle(0)

# ---------------------------------------------------------------------
# Command selection
# ---------------------------------------------------------------------

def get_command(robot_id, selector_motor):

    angle = selector_motor.angle() % 360

    if angle < 45 or angle >= 315:
        return "HOME"

    elif angle < 135:
        if robot_id == "ALL":
            return "BLUE"
        else:                   # ALL
            return "RED"

    elif angle < 225:
        return "GREEN"

    else:
        if robot_id == "ALL":
            return "RED"
        else:                   # ALL
            return "BLUE"


def send_command(robot_id, selector_motor):
    global counter

    counter += 1

    command = get_command(robot_id, selector_motor)
    message = (robot_id, command, counter)

    hub.ble.broadcast(message)
    print("sent:", message)

# ---------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------

while True:

    house_pressed = house_button.force() >= 0.1
    all_pressed = all_button.force() >= 0.1

    if house_pressed and not house_was_pressed:
        send_command("HOUSE", house_selector)

    if all_pressed and not all_was_pressed:
        send_command("ALL", all_selector)

    house_was_pressed = house_pressed
    all_was_pressed = all_pressed

    wait(50)
