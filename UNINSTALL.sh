#!/bin/sh

echo Removing start binary
sudo rm /bin/librepunch
echo Removing program files
sudo rm -rf $HOME/.librepunch
echo Removing auto start
sudo rm /etc/profile.d/start_libre.sh
echo "Uninstall complete"
