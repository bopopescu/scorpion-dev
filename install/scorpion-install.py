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
import os
import argparse

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

# Set IP Address?
set_ipv4 = True
set_ipv6 = True
set_localhost = True

# Install Gitlab
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
# Set IP Address
#################################################################

# Set the IPv4 Address
if set_ipv4:
    print('*' * 65)
    print " Setting IPv4 Address"
    get_ipv4 = "/sbin/ifconfig eth0 | awk '/inet / { print $2 }' | sed 's/addr://'"
    ipv4address = os.system(get_ipv4)
    set_ipv4_command = "echo %s %s %s >> /etc/hosts" % (ipv4address, FQDN, HOSTNAME)
    os.system(set_ipv4_command)
    print " Set IPv4 to %s." % ipv4address
    print('*' * 65)

# Set the IPv6 Address
if set_ipv6:
    print('*' * 65)
    print " Setting IPv6 Address"
    get_ipv6 = "/sbin/ifconfig eth0 | awk '/inet6 / { print $3;exit; }' | sed 's/addr:// '"
    ipv6address = os.system(get_ipv6)
    set_ipv6_command = "echo %s %s %s >> /etc/hosts" % (ipv6address, FQDN, HOSTNAME)
    os.system(set_ipv6_command)
    print " Set IPv6 to %s." % ipv6address
    print('*' * 65)

# Set the localhost Address
if set_localhost:
    print('*' * 65)
    print " Setting localhost Address"
    set_localhost_command = "echo 127.0.0.1 %s >> /etc/hosts" % HOSTNAME
    os.system(set_localhost_command)
    print " Set localhost with hostname %s." % HOSTNAME
    print('*' * 65)


#################################################################
# GitLab Install
#################################################################

# Kick off another script
# os.system('python hello.py')

# Begin Gitlab install
if gitlab_install:
    os.system("sudo apt-get -y install openssh-server")
    os.system("sudo apt-get -y install postfix")

    os.system("wget https://downloads-packages.s3.amazonaws.com/ubuntu-14.04/gitlab_7.8.4-omnibus-1_amd64.deb")
    os.system("sudo dpkg -i gitlab_7.8.4-omnibus-1_amd64.deb")

    os.system("sudo gitlab-ctl reconfigure")


#################################################################
# Post install cleanup
#################################################################

print('Complete')

try:
    os.remove('scorpion-install.py')
except OSError:
    pass