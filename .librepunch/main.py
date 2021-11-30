#!/bin/python3
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

class logger:

    logfile = "" # string // name of log file

    def __init__(self, logfile):
        ''' save logging settings '''
        self.logfile = logfile

    def addVars(self, string, varibles):
        ''' add varibles to a string '''
        arr = string.split('%')
        i = 1
        while i < len(arr):
            if arr[i] in varibles:
                arr[i] = varibles[arr[i]]
            else:
                arr[i] = "(NULL VARIABLE)"
            i += 2
        return ''.join(arr)

    def log(self, logstring, varibles):
        logString = self.addVars(logstring, varibles)
        f = open(self.logfile, 'a')
        f.write(logString + "\n")
        f.close()

# global varibles
import settings

def get_vars(start_vars = {}):
    out = start_vars
    cur = time.localtime()
    out['year'] = str(cur.tm_year)
    out['month'] = str(cur.tm_mon)
    out['day'] = str(cur.tm_mday)
    out['hour'] = str(cur.tm_hour)
    out['minute'] = str(cur.tm_min)
    out['second'] = str(cur.tm_sec)
    return out



def setFontSizes(w, h):
    titleFont = pygame.font.SysFont(settings.FONT_NAME, int(h * 0.0625))
    scanFont = pygame.font.SysFont(settings.FONT_NAME, int(w * 0.0625))
    loggedTitle = pygame.font.SysFont(settings.FONT_NAME, int(w * 0.04375))
    loggedUsers = pygame.font.SysFont(settings.FONT_NAME, int(w * 0.03125))
    copyTxt     = pygame.font.SysFont(settings.FONT_NAME, int(w * 0.015))
    return titleFont, scanFont, loggedTitle, loggedUsers, copyTxt

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

    if pin == settings.MANAGEMENT_PIN:

        logger.log(settings.SYSTEM_EXIT, get_vars())

        exit()

    elif pin == settings.ADMIN_PIN:

        # prepare to log out all users
        user_data = shelve.open(settings.USER_DATABASE)


        # log out all users
        temp = list(Logged_Users.keys())
        for i in temp:
            del Logged_Users[i]
            logger.log(settings.CLOCK_OUT, get_vars({"username" : user_data[i], "user_pin" : i}))
        
        printd(display, "Logged out all users")

    else:

        #check pin
        user_data = shelve.open(settings.USER_DATABASE)
        if pin in user_data.keys():

            if pin in Logged_Users.keys():
                del Logged_Users[pin]
                logger.log(settings.CLOCK_OUT, get_vars({"username" : user_data[pin], "user_pin" : pin}))

            else:
                Logged_Users[pin] = user_data[pin]
                logger.log(settings.CLOCK_IN, get_vars({"username" : user_data[pin], "user_pin" : pin}))

        else:

            printd(display, settings.INV_PIN)


def mainLoop():
    
    # init pygame window
    pygame.init()
    display = pygame.display.set_mode(settings.RESOLUTION, pygame.FULLSCREEN)#, pygame.RESIZABLE)
    pygame.display.set_caption('librepunch')
    log = logger(settings.USER_LOG)
    log.log(settings.SYSTEM_BOOT, get_vars())

    
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
                    handlePin(display, settings.PIN_HASHING_FCN(pin), Logged_Users, log)
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
        pin = settings.PIN_HASHING_FCN(sys.argv[2])
        if pin in user_data.keys():
            
            # change their name
            print("changing username for " + pin + " to " + sys.argv[3] + ".")
            user_data[pin] = sys.argv[3]
            user_data.sync()
            print("complete")

        else:
            
            # add new user
            print("Adding user " + pin + " : " + sys.argv[3] + ".")
            user_data[pin] = sys.argv[3]
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
        if settings.PIN_HASHING_FCN(sys.argv[2]) in user_data.keys():
            del user_data[settings.PIN_HASHING_FCN(sys.argv[2])]
            user_data.sync()
            print("User deleted")
        else:
            print("Error: No such user " + sys.argv[2])
    elif len(sys.argv) > 3:

        print ("too main arguements")

    else:

        print("too few arguements")

def chngSetPin(pin_name):
    f = open("settings.py", 'r')
    page = f.read().split("\n")
    f.close()
    for i in range(len(page)):
        if pin_name in page[i].split("#")[0]:
            page[i] = pin_name + " = \"" + str(settings.PIN_HASHING_FCN(sys.argv[2])) + "\""
            if len(page[i].split("#")) > 1:
                page[i] += page[i].split("#")[1]
    content = '\n'.join(page)
    f = open("settings.py", 'w')
    f.write(content)
    f.close()

def chngAdmPin():
    chngSetPin("ADMIN_PIN")

def chngManPin():
    chngSetPin("MANAGEMENT_PIN")

def checkFlags():

    # native flag list for librepunch
    flagList = {"-s" : mainLoop,"-l" : listUsers, "-n" : newDataBase, '-e' : editUsers, "-d" : deleteUser, '-a' : chngAdmPin, '-A' : chngManPin}

    if len(sys.argv) < 2:

        print("[librepunch]$ Error: librepunch must take at lest one flag to run")

    elif sys.argv[1] in flagList.keys():
        flagList[sys.argv[1]]()


def init():

    checkFlags()

if __name__ == "__main__":

    #ensure that we're not imported
    init()
