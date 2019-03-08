import socket
import time
from controller import Controller, Button, Direction, Stick


SERVER = "irc.twitch.tv"
PORT = 6667
PASS = "oauth:k52pshs0pdyrfsb0du6nb6pa191s7f"
BOT = "SmashBot"
CHANNEL = "twitchplayssmashultimate"
OWNER = "LittlestAnt"
irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send(("PASS " + PASS + "\n" +
          "NICK " + BOT + "\n" +
          "JOIN #" + CHANNEL + "\n").encode())

control = Controller('/Users/eminguyen/Library/Application Support/Dolphin/Pipes/pipe1')

def joinChat():
    loading = True
    while loading:
        readbuffer_join = irc.recv(1024).decode()
        for line in readbuffer_join.split("\n")[0:-1]:
            print(line)
            loading = loadingComplete(line)

def loadingComplete(line):
    if("End of /NAMES list" in line):
        print("Bot has joined " + CHANNEL + "'s channel")
        return False
    return True

def sendMessage(irc, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    irc.send((messageTemp + "\n").encode())

def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user

def getMessage(line):
    try:
        message = line.split(":", 2)[2]
    except:
        message = ""
    return message

def press_key(key, n_times = 1):
    for _ in range(n_times):
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)

while True:
    try:
        readbuffer = irc.recv(1024).decode()
    except:
        readbuffer = ""
    for line in readbuffer.split("\r\n")[0:-1]:
        if line == "":
            continue
        else:
            message = getMessage(line)
            control.performCommand(message)


joinChat()
