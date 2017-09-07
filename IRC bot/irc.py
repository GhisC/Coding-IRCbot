#!/usr/bin/python3
import socket

# Variables definition
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net"
channel = "##testmybot"
tontonAdolf = "TontonAdolf"
admin = "Tanoshi"
exitcode = "Bye " + tontonAdolf

# Connexion
ircsock.connect((server, 6667))
ircsock.send(bytes("USER " + tontonAdolf + " " + tontonAdolf + " " + tontonAdolf + " " + tontonAdolf + "\n", "UTF-8"))
ircsock.send(bytes("NICK " + tontonAdolf + "\n", "UTF-8"))


# Join channel
def joinChannel(channel):
    ircsock.send(bytes("JOIN " + channel + "\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)


# Return ping
def ping():
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))


# Send a msg
def sendmsg(msg, target=channel):
    ircsock.send(bytes("PRIVMSG " + target + " :" + msg + "\n", "UTF-8"))


# Main function
def main():
    joinChannel(channel)
    sendmsg("I'm alive!")
    while 1:
        # Receiving information
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

        # Split received message
        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!', 1)[0][1:]
            message = ircmsg.split('PRIVMSG', 1)[1].split(':', 1)[1]

            # Choose an action
            if len(name) < 17:
                # Bot interaction
                if message.find('Hello bot') != -1:
                    sendmsg("Hello " + name + "!")
                # Ask bot to pm someone
                if message[:5].find('.tell') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                    else:
                        target = name
                        message = "Could not parse. The message should be in the format of '.tell [target] [message]' to work properly."
                    sendmsg(message, target)

                # Stopping the bot
                if name.lower() == admin.lower() and message.rstrip() == exitcode:
                    sendmsg("I'll be back")
                    ircmsg.send(bytes("QUIT \n", "UTF-8"))
                    return
        else:
            # Respond to ping
            if ircmsg.find("PING :") != -1:
                ping()

main()
