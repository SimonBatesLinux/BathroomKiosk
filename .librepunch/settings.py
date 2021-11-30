
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
import hashlib

# message outputs
SCN_MSG = "Scan here:"
LOG_MSG = "Logged In:"
INV_PIN = "Invlid Pin.\n Please contact IT for assistance."

# LOG OUTPUTS
CLOCK_IN = "[%year%/%month%/%day%\t|\t%hour%:%minute%:%second%] - %username%:%user_pin% clocked in."
CLOCK_OUT = "[%year%/%month%/%day%\t|\t%hour%:%minute%:%second%] - %username%:%user_pin% clocked out."
SYSTEM_BOOT = "\t---\tprogram start on [%year%/%month%/%day%\t|\t%hour%:%minute%:%second%]\t---"
SYSTEM_EXIT = "\t---\tprogram exit on [%year%/%month%/%day%\t|\t%hour%:%minute%:%second%]\t---"


# program files
USER_DATABASE = "program_data/user.dat"
USER_LOG = "user_login.log"

# color option
BACKGROUND_COLOR = (255, 255, 255)
BACKGROUND_MSG_COL = (210,210,210)
LIBREPUNCH_BACKGROUND_TITLE_COL = (37, 116, 208)
LOGGED_BACKGROUND_COLOR = (220, 220, 220)

# font information
FONT_NAME = "sourcecodevariable"
SCN_COL = (0, 0, 0)
TITLE_COL = (255,255,255)
LOGGED_TITLE_COL = (0, 0, 0)
LOGGED_USERS_COL = (0, 0, 0)
MESSAGE_COL = (0, 0, 0)

# sizing
LOGGED_BAR_WIDTH = 0.35 # percent
TITLE_BAR_HEIGHT = 0.10 # percent
MESSAGE_MARGIN = 0.05 # percent

# screen settings
RESOLUTION = (0,0)

# pin settings
ADMIN_PIN = "123456789" # pin used to sign out all users
MANAGEMENT_PIN = "exit" # pin used to shutdown librepunch and manage a kiosk
def PIN_HASHING_FCN(pin):
    return pin
    # use for pin hashing with sha3 512
    # make sure to set admin and management pin with the -a and -A flags
    # see man page for more
    # return hashlib.sha3_512(pin.encode()).hexdigest()
