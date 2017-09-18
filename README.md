# MasterThesis

To enable autlogin (https://ubuntu-mate.community/t/enable-automatic-login-in-ubuntu-mate-16-04-for-raspberry-pi-3/5679/4)
nano /usr/share/lightdm/lightdm.conf.d/60-lightdm-gtk-greeter.conf
change:  autologin-user=[username]

To enable autologin for CLI (https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=145684)
sudo vi /etc/systemd/system/getty.target.wants/getty@tty1.service
Find the line 'ExecStart=-/sbin/agetty %I $TERM
Change it to 'ExecStart=-/sbin/agetty --noclear -a [username] %I $TERM

To run a terminal at launch
https://askubuntu.com/questions/756967/open-terminal-on-startup-and-run-command

If UAV is not connecting, go to /dev/ and see if /serial/ is a directory there.  That is where it looks for the UAV ID to connect.
If it is absent, reboot the uav with it unplugged from the PI, and let it sit for a moment before connecting it.