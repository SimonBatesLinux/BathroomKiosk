#/bin/sh

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

# dependencies
echo "Installing dependencies"
sudo apt upgrade zsh
sudo apt upgrade python3
sudo apt upgrade pip
sudo pip install pygame

# install command
echo "Installing command"
sudo cp librepunch /bin/librepunch
sudo chmod u=rwx,g=rx,o=rx /bin/librepunch

# complete program files
echo "Installing program files"
mkdir -p $HOME/.librepunch/program_data 2> /dev/null
cp .librepunch/main.py $HOME/.librepunch
cp .librepunch/settings.py $HOME/.librepunch
cp .librepunch/help.txt $HOME/.librepunch

#auto start application
echo "setting application to auto start"
sudo cp start_libre.sh /etc/profile.d
sudo cp .xinitrc $HOME
echo "Program installed, copy the ~/.librepunch direcory to backup librepunch"
