#!/bin/sh
#    librepunch  Copyright (C) 2021 Simon Bates

#    This file is part of librepunch.

#    librepunch is free software: you can redistribute it and/or modify

#    it under the terms of the GNU General Public License as published by

#    the Free Software Foundation, either version 3 of the License, or

#    (at your option) any later version.



#    librepunch is distributed in the hope that it will be useful,

#    but WITHOUT ANY WARRANTY; without even the implied warranty of

#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

#    GNU General Public License for more details.



#    You should have received a copy of the GNU General Public License

#    along with librepunch.  If not, see <https://www.gnu.org/licenses/>.

echo Removing start binary
sudo rm /bin/librepunch
echo Removing program files
sudo rm -rf $HOME/.librepunch
echo Removing auto start
sudo rm /etc/profile.d/start_libre.sh
echo "Uninstall complete"
