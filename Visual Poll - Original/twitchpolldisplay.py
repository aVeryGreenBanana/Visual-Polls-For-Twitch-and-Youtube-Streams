# All the twitch connection code is done by DougDoug and his team. 
# The visual additions, tallying, and all non twitch connection code is done by aVeryGreenBanana


# Things to note: (If you have trouble finding each line, just search for the line using the text in brackets next to it)
# 1. +start typed in twitch chat to open the pygame window
# 2. +next typed in twitch chat to go to next question
# 3. Change the RGB values in line 157 to change color values of the background (window.fill((0, 71, 187)))
# 4. Change RGB values on line 176 to change the color of the box that indicates most votes (pygame.draw.rect(window, (255, 165, 0))
# 5. Refer to line 36 to find where to add questions, image address, and the format it should follow (# Set up the poll options)
# 6. Make sure to change twitch_channel name on line 221 (TWITCH_CHANNEL = 'averygreenbanana')
# 7. Make sure to add names of your mods on line 95 to allow them to utilize the +start/+next commands (listOfMods = [TWITCH_CHANNEL, "mod1"])

import pygame
import sys
import concurrent.futures
import random
import keyboard
import pydirectinput
import pyautogui
import TwitchPlays_Connection
from TwitchPlays_KeyCodes import *

# Set up the message queue variables
MESSAGE_RATE = 0.5
MAX_QUEUE_LENGTH = 20
MAX_WORKERS = 100

last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []
pyautogui.FAILSAFE = False
alreadyVoted = []

# Set up the poll options
poll_questions = [
    {
        "question": "Question 1",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "images": [
            pygame.image.load('images/option1.png'),
            pygame.image.load('images/option2.png'),
            pygame.image.load('images/option3.png'),
            pygame.image.load('images/option4.png')
        ]
    },
    {
        "question": "Question 2",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "images": [
            pygame.image.load('images/optionA.png'),
            pygame.image.load('images/optionB.png'),
            pygame.image.load('images/optionC.png'),
            pygame.image.load('images/optionD.png')
        ]
    },
    {
        "question": "Question 3",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "images": [
            pygame.image.load('images/option1.png'),
            pygame.image.load('images/option2.png'),
            pygame.image.load('images/option3.png'),
            pygame.image.load('images/option4.png')
        ]
    },
    # Add more poll questions here
    # ...
    {
        "question": "Question 7",
        "options": ["Red", "Green", "Blue", "Yellow"],
        "images": [
            pygame.image.load('images/option4.png'),
            pygame.image.load('images/option2.png'),
            pygame.image.load('images/option3.png'),
            pygame.image.load('images/option1.png')
        ]
    }
]

# Initialize the vote counts
vote_counts = [{option: 0 for option in poll['options']} for poll in poll_questions]

# Set the current poll index to start at question 1
current_poll_index = 0

def handle_message(message):
    global vote_counts, current_poll_index, poll_questions, alreadyVoted

    try:
        msg = message['message'].lower()
        username = message['username'].lower()

        listOfMods = [TWITCH_CHANNEL, "mod1"] 

        if msg.isnumeric() and username not in alreadyVoted:
            # Convert the message to an integer
            vote = int(msg)
            if current_poll_index >= 0 and vote in range(1, len(poll_questions[current_poll_index]['options']) + 1):
                # Increment the vote count for the corresponding option
                option = poll_questions[current_poll_index]['options'][vote - 1]
                vote_counts[current_poll_index][option] += 1
                alreadyVoted.append(username)
                #print(alreadyVoted)
                #print(f"{username} voted for {option}")

        if username in listOfMods:
            if msg == "+start":
                if not pygame.display.get_init():
                    pygame.init()
                    start_visual_poll()

            elif msg == "+next":
                if current_poll_index + 1 < len(poll_questions):
                    current_poll_index += 1
                    alreadyVoted.clear()
                    reset_vote_counts()
                    #print("Next poll started")

    except Exception as e:
        print("Encountered exception: " + str(e))

def reset_vote_counts():
    global vote_counts
    vote_counts = [{option: 0 for option in poll['options']} for poll in poll_questions]

def start_visual_poll():
    # Set up the window
    window_width, window_height = 1000, 800  # Adjust window size as needed
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Visual Poll")

    # Set up fonts
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)
    result_font = pygame.font.Font(None, 30)

    # Set up the poll options
    option_height = 100
    option_spacing = 40  # Increase spacing between options
    option_image_size = (100, 100)

    options_start_y = window_height // 2 - ((len(poll_questions[current_poll_index]['options']) * (option_height + option_spacing)) // 2)

    # Load option images and scale them
    option_images = [pygame.transform.scale(image, option_image_size) for image in poll_questions[current_poll_index]['images']]

    # Game loop for the visual poll
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill((0, 71, 187))

        # Display poll title
        title_text = title_font.render(poll_questions[current_poll_index]['question'], True, (252, 252, 252))
        title_rect = title_text.get_rect(center=(window_width // 2, 50))
        window.blit(title_text, title_rect)

        # Display poll options and vote counts
        total_votes = sum(vote_counts[current_poll_index].values())
        start_y = options_start_y

        max_vote_count = max(vote_counts[current_poll_index].values())

        for i in range(len(poll_questions[current_poll_index]['options'])):
            option = poll_questions[current_poll_index]['options'][i]
            count = vote_counts[current_poll_index][option]

            # Highlight the option with the most votes in an orange box
            if count == max_vote_count and count != 0:
                pygame.draw.rect(window, (255, 165, 0), (40, start_y, window_width - 80, option_height))

            # Display option image
            image_rect = option_images[i].get_rect(midleft=(50, start_y + option_height // 2))
            window.blit(option_images[i], image_rect)

            # Display option text
            option_text = font.render(option, True, (252, 252, 252))
            option_rect = option_text.get_rect(midleft=(180, start_y + option_height // 2))
            window.blit(option_text, option_rect)

            # Calculate and display vote count and percentage
            if total_votes > 0:
                percentage = count / total_votes * 100
                result_text = result_font.render(f"{count} votes ({percentage:.1f}%)", True, (252, 252, 252))
            else:
                result_text = result_font.render("No votes", True, (252, 252, 252))

            result_rect = result_text.get_rect(midleft=(180, start_y + option_height // 2 + option_height // 4))
            window.blit(result_text, result_rect)

            start_y += option_height + option_spacing

        pygame.display.flip()

        # Check if there is a next question
        if current_poll_index < len(poll_questions):
            # Load the images for the next question
            next_option_images = [pygame.transform.scale(image, option_image_size) for image in poll_questions[current_poll_index]['images']]

            # Check if the next question has different number of options
            if len(next_option_images) != len(option_images):
                option_images = next_option_images
            else:
                # Check if the images for each option are different
                for i in range(len(option_images)):
                    if option_images[i] != next_option_images[i]:
                        option_images = next_option_images
                        break

    pygame.quit()
    sys.exit()


# Replace this with your Twitch username. Must be all lowercase.
TWITCH_CHANNEL = 'averygreenbanana'

# If streaming on Youtube, set this to False
STREAMING_ON_TWITCH = True

# Replace this with your Youtube's Channel ID
# Find this by clicking your Youtube profile pic -> Settings -> Advanced Settings
YOUTUBE_CHANNEL_ID = "YOUTUBE_CHANNEL_ID_HERE"

# If you're using an Unlisted stream to test on Youtube, replace "None" below with your stream's URL in quotes.
# Otherwise, you can leave this as "None"
YOUTUBE_STREAM_URL = None

# Count down before starting, so you have time to load up the game
countdown = 0
while countdown > 0:
    print(countdown)
    countdown -= 1
    time.sleep(1)

if STREAMING_ON_TWITCH:
    t = TwitchPlays_Connection.Twitch()
    t.twitch_connect(TWITCH_CHANNEL)
else:
    t = TwitchPlays_Connection.YouTube()
    t.youtube_connect(YOUTUBE_CHANNEL_ID, YOUTUBE_STREAM_URL)

# Set up the window flag
window_created = False

while True:
    active_tasks = [t for t in active_tasks if not t.done()]

    # Check for new messages
    new_messages = t.twitch_receive_messages()
    if new_messages:
        message_queue += new_messages
        message_queue = message_queue[-MAX_QUEUE_LENGTH:]

    messages_to_handle = []
    if not message_queue:
        last_time = time.time()
    else:
        r = 1 if MESSAGE_RATE == 0 else (time.time() - last_time) / MESSAGE_RATE
        n = int(r * len(message_queue))
        if n > 0:
            messages_to_handle = message_queue[0:n]
            del message_queue[0:n]
            last_time = time.time()

    if keyboard.is_pressed('shift+backspace'):
        exit()

    if not messages_to_handle:
        continue
    else:
        for message in messages_to_handle:
            if len(active_tasks) <= MAX_WORKERS:
                active_tasks.append(thread_pool.submit(handle_message, message))
            else:
                print(f'WARNING: active tasks ({len(active_tasks)}) exceeds number of workers ({MAX_WORKERS}). ({len(message_queue)} messages in the queue)')

    # Determine the selected option based on the maximum vote count
    if current_poll_index >= 0 and len(vote_counts[current_poll_index]) > 0:
        selected_option = max(vote_counts[current_poll_index], key=vote_counts[current_poll_index].get)
    else:
        selected_option = None

    # Print the current vote counts
    #print("Vote Counts:")
    #for option, count in vote_counts[current_poll_index].items():
    #    print(f"{option}: {count}")

    # If the visual poll is not running and there are votes, start the visual poll
    if selected_option is None and current_poll_index >= 0 and any(vote_counts[current_poll_index].values()):
        if not pygame.display.get_init():
            pygame.init()
            start_visual_poll()

    pygame.time.Clock().tick(60)

