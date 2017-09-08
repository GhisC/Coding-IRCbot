#!/usr/bin/python3
import socket


class IRCBot:
    def __init__(self):
        # Variables definition
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "chat.freenode.net"
        self.channel = "##testmybot"
        self.mybot = "Tonton"
        self.admin = "Tanoshi"
        self.exitcode = "Bye " + self.mybot

    def joinChannel(self, channel):
        # Connexion
        self.ircsock.connect((self.server, 6667))
        self.ircsock.send(
            bytes("USER " + self.mybot + " " + self.mybot + " " + self.mybot + " " + self.mybot + "\n", "UTF-8"))
        self.ircsock.send(bytes("NICK " + self.mybot + "\n", "UTF-8"))

        # Join channel
        self.ircsock.send(bytes("JOIN " + self.channel + "\n", "UTF-8"))
        ircmsg = ""
        while ircmsg.find("End of /NAMES list.") == -1:
            ircmsg = self.ircsock.recv(2048).decode("UTF-8")
            ircmsg = ircmsg.strip('\n\r')
            print(ircmsg)


    # Return ping
    def ping(self):
        self.ircsock.send(bytes("PONG :pingis\n", "UTF-8"))


    # Send a msg
    def sendmsg(self, msg, target=None):
        if target is None:
            target = self.channel
        self.ircsock.send(bytes("PRIVMSG " + target + " :" + msg + "\n", "UTF-8"))


    # Main function
    def main(self):
        self.joinChannel(self.channel)
        self.sendmsg("I'm alive!")
        while 1:
            # Receiving information
            ircmsg = self.ircsock.recv(2048).decode("UTF-8")
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
                        self.sendmsg("Hello " + name + "!")
                    # Ask bot to pm someone
                    if message[:5].find('.tell') != -1:
                        target = message.split(' ', 1)[1]
                        if target.find(' ') != -1:
                            message = target.split(' ', 1)[1]
                            print(message)
                            target = target.split(' ')[0]
                            print(target)
                        else:
                            target = name
                            message = "Could not parse. The message should be in the format of '.tell [target] [message]' to work properly."
                        self.sendmsg(message, target)

                    # Stopping the bot
                    if name.lower() == self.admin.lower() and message.rstrip() == self.exitcode:
                        self.sendmsg("I'll be back")
                        ircmsg.send(bytes("QUIT \n", "UTF-8"))
                        return
            else:
                # Respond to ping
                if ircmsg.find("PING :") != -1:
                    self.ping()

tonton = IRCBot()
tonton.main()
