#################################################################
#
#        Scorpion Server Manager
#
#             (        )
#             O        O
#             ()      ()
#              Oo.nn.oO
#               _mmmm_
#             \/_mmmm_\/
#             \/_mmmm_\/
#             \/_mmmm_\/
#             \/ mmmm \/
#                 nn
#                 ()   scorpion.io
#                 ()
#                  ()    /
#                   ()__()
#                    '--'
#
# Copyright (c) 2014 the scorpion.io authors. All rights reserved.
# Use of this source code is governed by a MIT license that can be
# found in the LICENSE file.
#
#################################################################

# Python module imports
import argparse
import os
import subprocess

# Make input compatible with Python 3
try: input = raw_input
except NameError: pass


#################################################################
# Install options
#################################################################

# Allow the script to move forward regardless of compatibility issues.
devmode = True

# Update OS
os_update = False

# Set Hostname
set_hostname = True

# Networking
set_ipv4 = True
set_ipv6 = True
set_localhost = True
restart_net_interfaces = True

# Software Installs
scorpion_install = True
postfix_install = True
mysql_install = True
php_install = True
nginx_install = True
supporting_software_install = True
gitlab_install = False


#################################################################
# Kick off installation
#################################################################

print('''
    Installing Scorpion Server Manager

             (        )
             O        O
             ()      ()
              Oo.nn.oO
               _mmmm_
             \/_mmmm_\/
             \/_mmmm_\/
             \/_mmmm_\/
             \/ mmmm \/
                 nn
                 ()   scorpion.io
                 ()
                  ()    /
                   ()__()
                    '--'
''')


#################################################################
# Check Python and OS version
#################################################################

# Check if dev mode or not.
if not devmode:
    # Check if Python is > 2.7
    if sys.version_info[:2] < (2, 7):
        print('*' * 65)
        print '''
        scorpion does not support python versions less than 2.7

        We have validated that scorpion works on the following systems
           * Ubuntu 14.04
        '''
        print('#' * 65)
        sys.exit(1)

    # Check if windows
    if platform.system() == 'Windows':
        print('#' * 65)
        print '''
        scorpion does not support windows

        We have validated that scorpion works on the following systems
           * Ubuntu 14.04
        '''
        print('#' * 65)
        sys.exit(1)

    # Check if Mac
    if platform.system() == 'Darwin':
        print('#' * 65)
        print '''
        scorpion does not support OS X

        We have validated that scorpion works on the following systems
           * Ubuntu 14.04
        '''
        print('#' * 65)
        sys.exit(1)


#################################################################
# Command line arguments
#################################################################

# Get the arguments from the command line
parser = argparse.ArgumentParser(description='Required information for script to setup scorpion.')
parser.add_argument('--aws-access-key-id')
parser.add_argument('--aws-secret-access-key')
parser.add_argument('--hostname')
parser.add_argument('--fqdn')
parser.add_argument('--password')
parser.add_argument('--serial')

# Parse the arguments
args = parser.parse_args()

# Get data from the parsed arguments
AWS_AKID = args.aws_access_key_id
AWS_SAK = args.aws_secret_access_key
HOSTNAME = args.hostname
FQDN = args.fqdn
PASSWORD = args.password
SERIAL = args.serial


#################################################################
# Check Variables.  If not supplied, request input.
#################################################################

if not AWS_AKID:
    AWS_AKID = input('Enter your AWS Access Key ID: ')

if not AWS_SAK:
    AWS_SAK = input('Enter your AWS Secret Access Key: ')

if not HOSTNAME:
    HOSTNAME = input('Enter the hostname you would like to use: ')

if not FQDN:
    FQDN = input('Enter the FQDN (fully qualified domain name you would like to use: ')

if not PASSWORD:
    PASSWORD = input('Enter the password you would like to use: ')


#################################################################
# Update OS
#################################################################

if os_update:
    os.system("sudo apt-get update")
    os.system("sudo apt-get upgrade -y")


#################################################################
# Set Hostname
#################################################################

if set_hostname:
    hostnameupdatestring = "echo %s > /etc/hostname" % HOSTNAME
    os.system(hostnameupdatestring)
    os.system("hostname -F /etc/hostname")


#################################################################
# Network Setup
#################################################################

# Set the IPv4 Address
if set_ipv4:
    print('*' * 65)
    print " Setting IPv4 Address"
    get_ipv4 = "ifconfig eth0 | awk '/inet / { print $2 }' | sed 's/addr://'"
    ipv4address = subprocess.check_output(get_ipv4, shell=True)
    ipv4address = ipv4address[:-1]
    set_ipv4_command = "echo %s %s %s >> /etc/hosts" % (ipv4address, FQDN, HOSTNAME)
    os.system(set_ipv4_command)
    print " Set IPv4 to %s" % ipv4address
    print('*' * 65)

# Set the IPv6 Address
if set_ipv6:
    print('*' * 65)
    print " Setting IPv6 Address"
    get_ipv6 = "ifconfig eth0 | awk '/inet6 / { print $3;exit; }' | sed 's/\/64// '"
    ipv6address = subprocess.check_output(get_ipv6, shell=True)
    ipv6address = ipv6address[:-1]
    set_ipv6_command = "echo %s %s %s >> /etc/hosts" % (ipv6address, FQDN, HOSTNAME)
    os.system(set_ipv6_command)
    print " Set IPv6 to %s" % ipv6address
    print('*' * 65)

# Set the localhost Address
if set_localhost:
    print('*' * 65)
    print " Setting localhost Address"
    set_localhost_command = "echo 127.0.0.1 %s >> /etc/hosts" % HOSTNAME
    os.system(set_localhost_command)
    print " Set localhost with hostname %s." % HOSTNAME
    print('*' * 65)

# Restart network interfaces
if restart_net_interfaces:
    print('*' * 65)
    print " Setting localhost Address"
    os.system("ifdown -a")
    os.system("ifup -a")
    os.system("ifup eth0")


#################################################################
# Scorpion Core Install
#################################################################

# Install scorpion requirements
if not os.path.isdir("/scorpion"):
    # Install Git to version control scorpion core
    os.system("apt-get -y install git")
    # Make the directory scorpion will reside
    os.makedirs("/scorpion")
    # Git clone the core
    os.system("git clone https://github.com/scorpion/scorpion-dev.git /scorpion")
else:
    # Folder exists, so just update
    os.system("git -C /scorpion pull")


#################################################################
# Postfix Install
#################################################################

if postfix_install:
    # Prestage postfix questions with default answers
    os.system("echo 'postfix postfix/main_mailer_type select Internet Site' | debconf-set-selections")
    os.system("echo 'postfix postfix/mailname string localhost' | debconf-set-selections")
    os.system("echo 'postfix postfix/destinations string localhost.localdomain, localhost' | debconf-set-selections")

    # Kick off the install
    os.system("apt-get -y install postfix")
    os.system("/usr/sbin/postconf -e 'inet_interfaces = loopback-only'")


#################################################################
# MySQL Install
#################################################################

if mysql_install:
    # Make installer non-interactive
    os.system("export DEBIAN_FRONTEND=noninteractive")

    # Install MySQL
    os.system("apt-get -q -y install mysql-server")

    # Set MySQL Password
    os.system("mysqladmin -u root password %s") % PASSWORD

    # Secure the MySQL installation
    os.system("sh /scorpion/install/mysql_secure.sh %s") % PASSWORD


#################################################################
# PHP Install
#################################################################

if php_install:
    # Install PHP
    os.system("apt-get -y install php5-fpm php5-cli php5-curl php5-gd php5-mcrypt php5-mysql php5-sqlite php-apc php-pear php5-tidy php5-imap")

    # Fix PHP5-IMAP extension by creating symbolic link
    os.system("sudo ln -s ../../mods-available/imap.ini /etc/php5/fpm/conf.d/20-imap.ini")

    # Fix 502 Bad Gateway
    #sed -i 's@listen = /var/run/php5-fpm.sock@listen = 127.0.0.1:9000@g' /etc/php5/fpm/pool.d/www.conf


#################################################################
# NGINX Install
#################################################################

if nginx_install:
    os.system("apt-get -q -y install nginx")


#################################################################
# Helpful System Software
#################################################################

if supporting_software_install:
    os.system("apt-get -q -y install htop imagemagick iftop mytop iptraf nmon lynx nmap screen monit mutt")


#################################################################
# GitLab Install
#################################################################

# Begin Gitlab install
if gitlab_install:
    os.system("sudo apt-get -y install openssh-server")
    os.system("sudo apt-get -y install postfix")

    os.system("wget https://downloads-packages.s3.amazonaws.com/ubuntu-14.04/gitlab_7.8.4-omnibus-1_amd64.deb")
    os.system("sudo dpkg -i gitlab_7.8.4-omnibus-1_amd64.deb")

    os.system("sudo gitlab-ctl reconfigure")


#################################################################
# Post Install Cleanup
#################################################################

print('Complete')

try:
    os.remove('scorpion-install.py')
except OSError:
    pass