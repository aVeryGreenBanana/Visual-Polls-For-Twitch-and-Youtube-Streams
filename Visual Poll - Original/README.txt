All the twitch connection code is done by DougDoug and his team. 
The visual additions, tallying, and all non connection/keycodes code is done by aVeryGreenBanana

Setup Instructions:

1. Install Python 3.9 from the windows store
2. Go to where the Visual Poll folder is located, open the folder and click the address bar (bar with file location/address), then type in cmd
3. this should bring up commmand prompt with file address already there
4. type in "pip install pyautogui" and hit enter, it should give you a message confirming that it was successfully installed
5. type in "pip install pygame" and hit enter, it should give you a message confirming that it was successfully installed    (probably not needed)                   
6. type in "pip install pydirectinput" and hit enter, it should give you a message confirming that it was successfully installed
7. type in "pip install pynput" and hit enter, it should give you a message confirming that it was successfully installed                     
8. type in "pip install keyboard" and hit enter, it should give you a message confirming that it was successfully installed
9. type in python twitchpolldisplay.py and hit enter (THIS IS HOW YOU'LL START THE PROGRAM IN FUTURE ITERATIONS)
10. if this works, you will be greeted with the message "connected to twitch.tv!" you are all set here. (do not close command prompt as this will stop the connection)
10.5 if this doesnt work and it says a module is missing, type 'pip install module_name' so if it says that the module missing is 'sleep' then type 'pip install sleep', then repeat step 9
11. Once done, click on command prompt, hit enter, then ctrl+c to stop the program, and close the pygame window. the last 2 lines should show "keyboardinterrupt   ^c"
    this means that the program was stopped successfully



Things to note/Things to change: (If you have trouble finding each line, just search for the line using the text in brackets next to it)

Mandatory Changes:
1. Make sure to change twitch_channel name on line 221 (TWITCH_CHANNEL = 'averygreenbanana')
2. Refer to line 36 to find where to add questions, image address, poll options, and the format it should follow (# Set up the poll options) 
3. Refer to the images folder to add images, and make sure that the file names correspond to the names typed. Like so: pygame.image.load('images/option1.png'),
4. Make sure to add names of your mods on line 95 to allow them to utilize the +start/+next commands (listOfMods = [TWITCH_CHANNEL, "mod1"])
5. Make sure to copy the spaces too when adding new lines if done via a .txt. This will prevent indentation errors from occuring. Simply hitting space will not do here
6. Once the program is running. +start typed in twitch chat to open the pygame window
7. While program is running, and pygame window is open, +next typed in twitch chat to go to next question

Visual Changes:
8. Change the RGB values in line 157 to change color values of the background (window.fill((0, 71, 187)))
9. Change RGB values on line 176 to change the color of the box that indicates most votes (pygame.draw.rect(window, (255, 165, 0))

If you have any questions, feel free to reach out at: https://twitter.com/VGreenBanana
