# Project64 Chaos
import random
import time
import keyboard

# Instructions: Create your save states in advance and saved to a backup folder for future use
#               Make sure to have Project64 in focus before pressing enter
#               It will start 2 seconds after pressing enter and exit when you press escape
#               You can also use the space button to remove the current state from the rotation
#               You can also adjust the range for the random shuffle times or change it
#               to move through the states sequentially if you want

# Settings
save_states = 4  # Number of save_states to cycle between up to 9
minimum_wait = 2  # Minimum time before changing save states
maximum_wait = 25  # Maximum wait time before changing save states
mode = 'random'  # random or sequential(default)
finished_list = set()  # Set containing completed states
running = True


def complete_state(keyb):
    # Pressing space will remove the current state from rotation...
    # Hopefully you don't press it right as it's switching. It doesn't have a buffer
    global finished_list
    finished_list.add(state)
    print("Finished State: %d" % state)


def exit_program(keyb):
    global running
    print("Exiting")
    running = False


def random_wait():
    wait_time = random.randrange(minimum_wait, maximum_wait + 1)  # Determine random wait time
    print("You have %d seconds! Good Luck" % wait_time)
    time.sleep(wait_time)


keyboard.on_press_key('space', complete_state)
keyboard.on_press_key('esc', exit_program)

keyboard.wait('enter')  # Wait for Enter to be Pressed
print('Hey Bozo!')
time.sleep(2)  # 2 seconds to let user click onto window

state = 1  # initial state

# Start on the first State
keyboard.press('1')  # Set State 1
time.sleep(.1)
keyboard.press('f7')  # Load State 1
random_wait()


while (len(finished_list) < save_states) & running:
    previous_state = state

    if mode == 'random':
        # Find a random state other than the current 1
        while state == previous_state or state in finished_list:
            state = random.randrange(save_states) + 1  # Get a random number from 0 to X
    else:
        state = state % save_states + 1
        while state in finished_list:
            state = state % save_states + 1

    keyboard.press('f5')  # Save the current state
    time.sleep(.1)
    keyboard.press(str(state))  # Switch to new state
    print("New State: %d" % state)
    time.sleep(.1)
    keyboard.press('f7')
    random_wait()
