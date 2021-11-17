"""

    librepunch  Copyright (C) 2021 Simon Bates

    This file is part of librepunch.

    librepunch is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    librepunch is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with librepunch.  If not, see <https://www.gnu.org/licenses/>.

"""

# import packages
import sys
import time
import shelve
import pygame
import os

# global varibles
import settings

def setFontSizes(w, h):
    titleFont = pygame.font.SysFont(settings.FONT_NAME, int(h * 0.0625))
    scanFont = pygame.font.SysFont(settings.FONT_NAME, int(w * 0.0625))
    loggedTitle = pygame.font.SysFont(settings.FONT_NAME, int(w * 0.04375))
    loggedUsers = pygame.font.SysFont(settings.FONT_NAME, int(w * 0.03125))
    copyTxt     = pygame.font.SysFont(settings.FONT_NAME, int(w * 0.015))
    return titleFont, scanFont, loggedTitle, loggedUsers, copyTxt

class logger:

    def __init__(self):
        if not os.path.isfile(settings.USER_LOG):
            f = open(settings.USER_LOG, 'w')
            f.write("")
            f.close()

    def log(self, log):
        f = open(settings.USER_LOG, "a")
        f.write(log + "\n")
        f.close()


def printd(display, message):
    upMessage = True
    while upMessage:

        # check all events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    upMessage = False

            # get screen information
            w, h = pygame.display.get_surface().get_size()
        
            # message background
            pygame.draw.rect(display, settings.BACKGROUND_MSG_COL, [w * settings.MESSAGE_MARGIN, h * settings.MESSAGE_MARGIN, w - (w * settings.MESSAGE_MARGIN * 2), h - (h * settings.MESSAGE_MARGIN * 2)])

            # display message
            messageFont = pygame.font.SysFont(settings.FONT_NAME, int(w * 0.03125))
            msg = message.split("\n")
            lineCT = len(msg)
            lines = []
            for i in msg:
                lines.append(messageFont.render(i, True, settings.MESSAGE_COL))

            totalH = lines[0].get_height() * lineCT

            y = ((h - (h * settings.MESSAGE_MARGIN)) - totalH) / 2
            for i in lines:
                x = ((w - (w * settings.MESSAGE_MARGIN)) - i.get_width()) / 2
                display.blit(i, (x,y))
                y += i.get_height()
        
            pygame.display.flip()

def handlePin(display, pin, Logged_Users, logger):

    if pin == "exit":

        # open management terminal
        exit()

    elif pin == settings.ADMIN_PIN:

        # prepare to log out all users
        cur = time.localtime()
        curTime = str(cur.tm_mday) + "/" + str(cur.tm_mon) + "/" + str(cur.tm_year) + "   " + str(cur.tm_hour) + ":" + str(cur.tm_min) + ":" + str(cur.tm_sec)
        user_data = shelve.open(settings.USER_DATABASE)


        # log out all users
        temp = list(Logged_Users.keys())
        for i in temp:
            del Logged_Users[i]
            logger.log("[" + i + " : " + user_data[i] + "]: logged out at " + curTime + ".")
        
        printd(display, "Logged out all users")

    else:

        #check pin
        user_data = shelve.open(settings.USER_DATABASE)
        if pin in user_data.keys():
            
            cur = time.localtime()
            curTime = str(cur.tm_mday) + "/" + str(cur.tm_mon) + "/" + str(cur.tm_year) + "   " + str(cur.tm_hour) + ":" + str(cur.tm_min) + ":" + str(cur.tm_sec)
            
            if pin in Logged_Users.keys():
                del Logged_Users[pin]
                logger.log("[" + pin + " : " + user_data[pin] + "]: logged out at " + curTime + ".")

            else:
                Logged_Users[pin] = user_data[pin]
                logger.log("[" + pin + " : " + user_data[pin] + "]: logged in at " + curTime + ".")

        else:

            printd(display, settings.INV_PIN)


def mainLoop():
    
    # init pygame window
    pygame.init()
    display = pygame.display.set_mode(settings.RESOLUTION, pygame.FULLSCREEN)#, pygame.RESIZABLE)
    pygame.display.set_caption('librepunch')
    log = logger()
    
    Logged_Users = {}

    firstLoop = True
    
    pin = ''

    running = True
    while running:

        # check all events
        for event in pygame.event.get():

            # if the window is closed
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                # get user input
                if event.key == pygame.K_RETURN:
                    handlePin(display, pin, Logged_Users, log)
                    pin = ''

                else:

                    pin += event.unicode

        # get screen information
        w, h = pygame.display.get_surface().get_size()
        
        # display
        display.fill(settings.BACKGROUND_COLOR) # background color
        pygame.draw.rect(display, settings.LIBREPUNCH_BACKGROUND_TITLE_COL, [0, 0, w, h * settings.TITLE_BAR_HEIGHT ]) # top bar
        pygame.draw.rect(display, settings.LOGGED_BACKGROUND_COLOR, [w - (w * settings.LOGGED_BAR_WIDTH), h * settings.TITLE_BAR_HEIGHT, w * settings.LOGGED_BAR_WIDTH, h - (h * settings.TITLE_BAR_HEIGHT)])
        
        # draw text
        titleFont, scanFont, loggedTitle, loggedUsers, copyTxt = setFontSizes(w, h)

            # background text

        scanTxt = scanFont.render(settings.SCN_MSG, True, settings.SCN_COL)# draw scan message
        display.blit(scanTxt, ((w - (w * settings.LOGGED_BAR_WIDTH) - scanTxt.get_width()) / 2, (h - (h * settings.TITLE_BAR_HEIGHT) - scanTxt.get_height()) / 2))

        titleTxt = titleFont.render('librepunch', True, settings.TITLE_COL)# draw title name
        display.blit(titleTxt, (0,0))

        logTitle = loggedTitle.render(settings.LOG_MSG, True, settings.LOGGED_TITLE_COL) # draw logged in title
        display.blit(logTitle, (w - (w * settings.LOGGED_BAR_WIDTH), (h * settings.TITLE_BAR_HEIGHT)))
        
        y = h * settings.TITLE_BAR_HEIGHT + logTitle.get_height()

        for i in list(Logged_Users.keys()):
            userTxt = loggedUsers.render(Logged_Users[i], True, settings.LOGGED_USERS_COL)
            display.blit(userTxt, (w - (w * settings.LOGGED_BAR_WIDTH), y))
            y += userTxt.get_height()
            
        #display.blit(GNU_LOGO, (0, h - 54))
        copyright = copyTxt.render(' librepunch  Copyright (C) 2021 Simon Bates ', True, (0, 0, 0))
        display.blit(copyright, (0, h - copyright.get_height()))

        # show changes to screen
        pygame.display.flip()

def listUsers():

    # list all users
    user_data = shelve.open(settings.USER_DATABASE)
    for i in list(user_data.keys()):

        print(i + " : " + user_data[i])

    print("End of database")

def newDataBase():

    perm = input("Warning! You are removing all users. Are you sure (y/n)?")
    if perm == "y":

        # del all user
        temp = []
        user_data = shelve.open(settings.USER_DATABASE)
        for i in list(user_data.keys()):

            temp.append(i)

        for i in temp:

            del user_data[i]

        print("database cleared")
    else:
        print("Aborting...")


def editUsers():

    if len(sys.argv) == 4:
        
        # check to see if the user already exists
        user_data = shelve.open(settings.USER_DATABASE)
        if sys.argv[2] in user_data.keys():
            
            # change their name
            print("changing username for " + sys.argv[2] + " to " + sys.argv[3] + ".")
            user_data[sys.argv[2]] = sys.argv[3]
            user_data.sync()
            print("complete")

        else:
            
            # add new user
            print("Adding user " + sys.argv[2] + " : " + sys.argv[3] + ".")
            user_data[sys.argv[2]] = sys.argv[3]
            user_data.sync()
            print("complete")


    elif len(sys.argv) > 4:

        print ("too main arguements")

    else:

        print("too few arguements")

def deleteUser():

    if len(sys.argv) == 3:
        # delete user
        user_data = shelve.open(settings.USER_DATABASE)
        if sys.argv[2] in user_data.keys():
            del user_data[sys.argv[2]]
            user_data.sync()
            print("User deleted")
        else:
            print("Error: No such user " + sys.argv[2])
    elif len(sys.argv) > 3:

        print ("too main arguements")

    else:

        print("too few arguements")
  
def helpPage():
    os.system("less help.txt")


def checkFlags():

    # native flag list for librepunch
    flagList = {"-s" : mainLoop,"-l" : listUsers, "-n" : newDataBase, '-e' : editUsers, "-d" : deleteUser, "-h" : helpPage, "-?" : helpPage, "help" : helpPage}

    if len(sys.argv) < 2:

        print("[librepunch]$ Error: librepunch must take at lest one flag to run")

    elif sys.argv[1] in flagList.keys():
        flagList[sys.argv[1]]()


def init():

    checkFlags()

if __name__ == "__main__":

    #ensure that we're not imported
    init()
