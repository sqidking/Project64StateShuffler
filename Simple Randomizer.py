import time
import random
import keyboard
from OBS_Websockets import OBSWebsocketsManager
from stopwatch import Stopwatch  # using stopwatch from py-stopwatch


# Instructions: Create your save states in advance and saved to a backup folder for future use
#               Make sure to have Project64 in focus before pressing enter
#               It will start 2 seconds after pressing enter and exit when you press escape
#               You can also use the space button to remove the current state from the rotation
#               You can also adjust the range for the random shuffle times or change it
#               to move through the states sequentially if you want

# CONSTANTS
SAVE_STATES = 4  # Number of save_states to cycle between up to 9
MINIMUM_WAIT = 2  # Minimum time before changing save states
MAXIMUM_WAIT = 25  # Maximum wait time before changing save states
MODE = 'random'  # random or sequential(default)
SPACEBAR_COOLDOWN = 2  # Number of seconds after a state switch where pressing space won't do anything
USING_OBS_WEBSOCKETS = True  # Whether program should display the # of remaining races in OBS
OBS_TEXT_SOURCE = "Timer_Box"  # Name this whatever text element you want to update in OBS

def complete_state(keyb):
    # Pressing space will remove the current state from rotation
    global finished_list, last_spacebar, manual_complete, SPACEBAR_COOLDOWN
    # Prevent pressing space multiple times messing things up and swapping too fast
    if time.time() - last_spacebar >= SPACEBAR_COOLDOWN and time.time() - last_swap > 1:
        last_spacebar = time.time()
        finished_list.add(state)
        manual_complete = True
        print("Finished State: %d" % state)

def exit_program(keyb):
    global running
    print("Exiting")
    running = False


##########################################################
print('Press Enter to begin!')
keyboard.wait('enter')  # Wait for Enter to be Pressed
print('Hey Bozo!')
time.sleep(2)  # A small wait

# Initialize Variables
finished_list = set()  # Set containing completed states
running = True
timer_complete = False
state_buffer = 1
last_spacebar = 0
last_swap = 0
state = 1  # initial state
first_call = True
multiple_slots_remain = True
manual_complete = False
timers = {}

keyboard.on_press_key('space', complete_state)
keyboard.on_press_key('esc', exit_program)

if USING_OBS_WEBSOCKETS:
    obswebsockets_manager = OBSWebsocketsManager()

while (len(finished_list) < SAVE_STATES) & running & multiple_slots_remain:
    if not first_call:
        previous_state = state

        if MODE == 'random':
            # Find a random state other than the current 1
            if len(finished_list) < SAVE_STATES:
                while state == previous_state or state in finished_list:
                    state = random.randrange(SAVE_STATES) + 1  # Get a random number from 1 to X
                if len(finished_list) == SAVE_STATES - 1:
                    multiple_slots_remain = False  # Lets this loop know to load last state and go down into idle loop
        else:
            state = state % SAVE_STATES + 1
            while state in finished_list:
                state = state % SAVE_STATES + 1
        keyboard.press('f5')  # Save the current state - skip this first time around
        time.sleep(.1)

    keyboard.press(str(state))  # Switch to new state
    print("New State: %d" % state)
    time.sleep(.1)
    keyboard.press('f7')

    # Start or Resume OBS Timer
    if state in timers:
        timers[state].resume()
    else:
        timers[state] = Stopwatch()
        timers[state].start()
    last_swap = time.time()

    wait_time = random.randrange(MINIMUM_WAIT, MAXIMUM_WAIT + 1)  # Determine random wait time
    print("You have %d seconds! Good Luck" % wait_time)
    waits = wait_time * 10
    for i in range(waits):
        time.sleep(0.1)
        if USING_OBS_WEBSOCKETS:
            timers[state].tick()
            m, s = divmod(timers[state].time_active, 60)
            h, m = divmod(m, 60)
            if h == 0:
                obswebsockets_manager.set_text(OBS_TEXT_SOURCE, f"{m:.0f}:{s:.2f}")
            else:
                obswebsockets_manager.set_text(OBS_TEXT_SOURCE, f"{h:.0f}:{m:.0f}:{s:.2f}")
        if not running or manual_complete:
            manual_complete = False
            break
    if multiple_slots_remain:
        timers[state].pause()

    first_call = False

# It will move into this loop when 1 state is left to prevent it from doing dumb stuff, this loop will handle
# the timer after the last random_wait until they press space for the last time
print('Last State!')

while (len(finished_list) < SAVE_STATES) & running:
    time.sleep(.1)
    timers[state].tick()
    if USING_OBS_WEBSOCKETS:
        m, s = divmod(timers[state].time_active, 60)
        h, m = divmod(m, 60)
        obswebsockets_manager.set_text(OBS_TEXT_SOURCE, f"{h:.0f}:{m:.0f}:{s:.2f}")
for i in range(SAVE_STATES):
    timers[i+1].tick()
    m, s = divmod(timers[i+1].time_active, 60)
    h, m = divmod(m, 60)
    if h == 0:
        print(f"{m:.0f}:{s:.2f}")
    else:
        print(f"{h:.0f}:{m:.0f}:{s:.2f}")

if running:
    print('You did it!')
else:
    print('You gave up! :(')
