#################################################################
##
##        Scorpion Server Manager
##
##             (        )
##             O        O
##             ()      ()
##              Oo.nn.oO
##               _mmmm_
##             \/_mmmm_\/
##             \/_mmmm_\/
##             \/_mmmm_\/
##             \/ mmmm \/
##                 nn
##                 ()   scorpion.io
##                 ()
##                  ()    /
##                   ()__()
##                    '--'
##
## Copyright (c) 2014 the scorpion.io authors. All rights reserved.
## Use of this source code is governed by a MIT license that can be
## found in the LICENSE file.
##
#################################################################

## Python imports and other
import os
import argparse

try: input = raw_input
except NameError: pass

#################################################################
## Install options
#################################################################

# Allow the script to move forward regardless of compatibility issues.
devmode = True
# Update OS
os_update = False
# Install Gitlab
gitlab_install = False

#################################################################
## Kick off installation
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
## Check Python and OS version
#################################################################

## Check if dev mode or not.
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

    ## Check if windows
    if platform.system() == 'Windows':
        print('#' * 65)
        print '''
        scorpion does not support windows

        We have validated that scorpion works on the following systems
           * Ubuntu 14.04
        '''
        print('#' * 65)
        sys.exit(1)

    ## Check if Mac
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
## Command line arguments
#################################################################

## Get the arguments from the command line
parser = argparse.ArgumentParser(description='AWS Credentials for saving and restoring backups.')
parser.add_argument('--aws-access-key-id')
parser.add_argument('--aws-secret-access-key')
parser.add_argument('--hostname')
parser.add_argument('--fqdn')
parser.add_argument('--password')

# Parse the arguments
args = parser.parse_args()

# Get data from the parsed arguments
AWS_AKID = args.aws_access_key_id
AWS_SAK = args.aws_secret_access_key
HOSTNAME = args.hostname
fqdn = args.fqdn
password = args.password

#################################################################
## Online backup setup
#################################################################

if not AWS_AKID:
    AWS_AKID = input('Enter your AWS Access Key ID: ')

if not AWS_SAK:
    AWS_SAK = input('Enter your AWS Secret Access Key: ')

## Show the AWS Keys
#print AWS_AKID
#print AWS_SAK

#################################################################
## Update OS
#################################################################

if os_update:
    os.system("sudo apt-get update")
    os.system("sudo apt-get upgrade -y")

#################################################################
## Set IP Address
#################################################################



#################################################################
## Set Hostname
#################################################################

hostnameupdatestring = "%s > /etc/hostname" % (hostname argument2)
os.system(hostnameupdatestring)

#################################################################
## GitLab Install
#################################################################

## Kick off another script
#os.system('python hello.py')

## Begin Gitlab install
if gitlab_install:
    os.system("sudo apt-get -y install openssh-server")
    os.system("sudo apt-get -y install postfix")

    os.system("wget https://downloads-packages.s3.amazonaws.com/ubuntu-14.04/gitlab_7.8.4-omnibus-1_amd64.deb")
    os.system("sudo dpkg -i gitlab_7.8.4-omnibus-1_amd64.deb")

    os.system("sudo gitlab-ctl reconfigure")

#################################################################
## Post install cleanup
#################################################################

print('Complete')

try:
    os.remove('scorpion-install.py')
except OSError:
    pass