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
import shutil
import subprocess
import tarfile
import urllib

# Make input compatible with Python 3
try: input = raw_input
except NameError: pass


#################################################################
# Install options
#################################################################

# Allow the script to move forward regardless of compatibility issues.
devmode = True

# Update OS
os_update = True
os_upgrade = False

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
nginx_install = True
apache_install = True
php_install = True
ioncube_install = True
gunicorn_install = True
supporting_software_install = True
gitlab_install = False
s3cmd_install = True

# Security Related
fail2ban_install = True
firewall_setup = True


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
# Functions used in script
#################################################################

def installMessageStart(installMessage):
    print('*' * 65)
    print " %s" % installMessage
    print ""

def installMessageEnd():
    print " Done"
    print('*' * 65)
    print ""


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
    installMessageStart("Starting apt-get Update")

    # Update the packages repo
    os.system("sudo apt-get -qq -y update")

    installMessageEnd()

if os_upgrade:
    installMessageStart("Updating OS")

    # Upgrade installed packages to latest versions
    subprocess.call("sudo apt-get -qq -y upgrade", stdout=None, shell=True)

    installMessageEnd()


#################################################################
# Set Hostname
#################################################################

if set_hostname:
    installMessageStart("Updating Hostname")

    hostnameupdatestring = "echo %s > /etc/hostname" % HOSTNAME
    subprocess.call(hostnameupdatestring, stdout=None, shell=True)
    subprocess.call("hostname -F /etc/hostname", stdout=None, shell=True)

    installMessageEnd()


#################################################################
# Network Setup
#################################################################

# Set the IPv4 Address
if set_ipv4:
    installMessageStart("Setting IPv4 Network Address")

    get_ipv4 = "ifconfig eth0 | awk '/inet / { print $2 }' | sed 's/addr://'"
    ipv4address = subprocess.check_output(get_ipv4, shell=True)
    ipv4address = ipv4address[:-1]
    set_ipv4_command = "echo %s %s %s >> /etc/hosts" % (ipv4address, FQDN, HOSTNAME)
    subprocess.call(set_ipv4_command, stdout=None, shell=True)

    installMessageEnd()

# Set the IPv6 Address
if set_ipv6:
    installMessageStart("Setting IPv6 Network Address")

    get_ipv6 = "ifconfig eth0 | awk '/inet6 / { print $3;exit; }' | sed 's/\/64// '"
    ipv6address = subprocess.check_output(get_ipv6, shell=True)
    ipv6address = ipv6address[:-1]
    set_ipv6_command = "echo %s %s %s >> /etc/hosts" % (ipv6address, FQDN, HOSTNAME)
    subprocess.call(set_ipv6_command, stdout=None, shell=True)

    installMessageEnd()

# Set the localhost Address
if set_localhost:
    installMessageStart("Setting localhost Network Address")

    set_localhost_command = "echo 127.0.0.1 %s >> /etc/hosts" % HOSTNAME
    subprocess.call(set_localhost_command, stdout=None, shell=True)

    installMessageEnd()

# Restart network interfaces
if restart_net_interfaces:
    installMessageStart("Restarting Network Interfaces")

    subprocess.call("ifdown -a", stdout=None, shell=True)
    subprocess.call("ifup -a", stdout=None, shell=True)
    subprocess.call("ifup eth0", stdout=None, shell=True)

    installMessageEnd()


#################################################################
# Scorpion Core Install
#################################################################

# Install scorpion requirements
if not os.path.isdir("/scorpion"):
    installMessageStart("Installing Git and downloading Scorpion Core")

    # Install Git to version control scorpion core
    subprocess.call("apt-get -qq -y install git", stdout=None, shell=True)
    # Make the directory scorpion will reside
    os.makedirs("/scorpion")
    # Git clone the core
    subprocess.call("git clone https://github.com/scorpion/scorpion-dev.git /scorpion", stdout=None, shell=True)

    installMessageEnd()

else:
    installMessageStart("Scorpion installed, updating core to latest version")

    # Folder exists, so just update
    subprocess.call("git -C /scorpion pull", stdout=None, shell=True)

    installMessageEnd()


#################################################################
# Postfix Install
#################################################################

if postfix_install:
    installMessageStart("Installing Postfix")

    # Prestage postfix questions with default answers
    subprocess.call("echo 'postfix postfix/main_mailer_type select Internet Site' | debconf-set-selections", stdout=None, shell=True)
    subprocess.call("echo 'postfix postfix/mailname string localhost' | debconf-set-selections", stdout=None, shell=True)
    subprocess.call("echo 'postfix postfix/destinations string localhost.localdomain, localhost' | debconf-set-selections", stdout=None, shell=True)

    # Kick off the install
    subprocess.call("apt-get -qq -y install postfix", stdout=None, shell=True)
    subprocess.call("/usr/sbin/postconf -e 'inet_interfaces = loopback-only'", stdout=None, shell=True)

    installMessageEnd()


#################################################################
# MySQL Install
#################################################################

if mysql_install:
    installMessageStart("Installing MySQL")

    # Make installer non-interactive
    mysql_pass_command1 = "echo 'mysql-server mysql-server/root_password password %s' | sudo debconf-set-selections" % PASSWORD
    mysql_pass_command2 = "echo 'mysql-server mysql-server/root_password_again password %s' | sudo debconf-set-selections" % PASSWORD
    subprocess.call(mysql_pass_command1, stdout=None, shell=True)
    subprocess.call(mysql_pass_command2, stdout=None, shell=True)

    # Install MySQL
    subprocess.call("apt-get -qq -y install mysql-server", stdout=None, shell=True)

    # Set MySQL Password
    mysql_password_set = "mysqladmin -u root password %s" % PASSWORD
    subprocess.call(mysql_password_set, stdout=None, shell=True)

    # Secure the MySQL installation
    mysql_install_secure = "sudo sh /scorpion/install/mysql_secure.sh %s" % PASSWORD
    subprocess.call(mysql_install_secure, stdout=None, shell=True)

    installMessageEnd()


#################################################################
# NGINX Install
#################################################################

if nginx_install:
    installMessageStart("Installing Nginx")

    # Installo Nginx
    subprocess.call("apt-get -qq -y install nginx", stdout=None, shell=True)

    installMessageEnd()


#################################################################
# Apache Install
#################################################################

if apache_install:
    installMessageStart("Installing Apache")

    # Install Apache
    subprocess.call("apt-get -qq -y install apache2", stdout=None, shell=True)

    # Copy proper Apache ports
    shutil.copyfile('/scorpion/install/ports.conf', '/etc/apache2/ports.conf')

    # Restart Apache
    subprocess.call("service apache2 restart", stdout=None, shell=True)

    installMessageEnd()


#################################################################
# PHP Install
#################################################################

if php_install:
    installMessageStart("Installing PHP")

    # Install PHP
    subprocess.call("apt-get -qq -y install php5 php5-cli php5-curl php5-gd php5-mcrypt php5-mysql php5-sqlite php-apc php-pear php5-tidy php5-imap", stdout=None, shell=True)

    # Fix PHP5-IMAP extension by creating symbolic link
    subprocess.call("sudo ln -s ../../mods-available/imap.ini /etc/php5/fpm/conf.d/20-imap.ini", stdout=None, shell=True)

    # Fix 502 Bad Gateway
    #sed -i 's@listen = /var/run/php5-fpm.sock@listen = 127.0.0.1:9000@g' /etc/php5/fpm/pool.d/www.conf

    installMessageEnd()


#################################################################
# Ioncube Install
#################################################################

if ioncube_install:
    installMessageStart("Installing Ioncube")

    # Download the ioncube loader for PHP
    urllib.urlretrieve('http://downloads3.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.gz','ioncube_loaders_lin_x86-64.tar.gz')

    # Extract the tar
    tar = tarfile.open("ioncube_loaders_lin_x86-64.tar.gz")
    tar.extractall()
    tar.close()

    # Copy / Install the PHP 5.5 version
    shutil.copyfile('ioncube/ioncube_loader_lin_5.5.so', '/usr/lib/php5/20121212/ioncube_loader_lin_5.5.so')

    # Add the extension to the php.ini file for both apache and cli
    subprocess.call("echo 'zend_extension = /usr/lib/php5/20121212/ioncube_loader_lin_5.5.so' >> /etc/php5/apache2/php.ini", stdout=None, shell=True)
    subprocess.call("echo 'zend_extension = /usr/lib/php5/20121212/ioncube_loader_lin_5.5.so' >> /etc/php5/cli/php.ini", stdout=None, shell=True)

    # Restart apache to make the change take affect
    subprocess.call("service apache2 restart", stdout=None, shell=True)

    # Cleanup - Remove the tar and the extracted contents
    os.remove('ioncube_loaders_lin_x86-64.tar.gz')
    shutil.rmtree('ioncube')

    installMessageEnd()


#################################################################
# Gunicorn Install
#################################################################

if gunicorn_install:
    installMessageStart("Installing Gunicorn")

    # Install Apache
    subprocess.call("apt-get -qq -y install gunicorn", stdout=None, shell=True)

    installMessageEnd()


#################################################################
# Helpful System Software
#################################################################

if supporting_software_install:
    installMessageStart("Installing Supporting Software")

    # Install Supporting Software
    subprocess.call("apt-get -qq -y install htop imagemagick iftop mytop iptraf nmon lynx nmap screen monit mutt", stdout=None, shell=True)

    installMessageEnd()


#################################################################
# GitLab Install
#################################################################

# Begin Gitlab install
if gitlab_install:
    installMessageStart("Installing Supporting Software")

    # Install required pre-requisites
    subprocess.call("apt-get -qq -y install openssh-server", stdout=None, shell=True)
    subprocess.call("apt-get -qq -y install postfix")

    # Download and install Gitlab
    subprocess.call("wget https://downloads-packages.s3.amazonaws.com/ubuntu-14.04/gitlab_7.8.4-omnibus-1_amd64.deb", stdout=None, shell=True)
    subprocess.call("sudo dpkg -i gitlab_7.8.4-omnibus-1_amd64.deb", stdout=None, shell=True)

    # Configure Gitlab
    subprocess.call("sudo gitlab-ctl reconfigure", stdout=None, shell=True)

    installMessageEnd()


#################################################################
# S3CMD Install (Amazon S3 Backup)
#################################################################

if s3cmd_install:
    installMessageStart("Installing S3CMD")

    # Install S3CMD
    subprocess.call("apt-get -qq -y install s3cmd", stdout=None, shell=True)

    # Set MySQL Password
    s3cmd_setup_command = "sudo sh /scorpion/install/s3cmd_config.sh %s %s" % (AWS_AKID, AWS_SAK)
    subprocess.call(s3cmd_setup_command, stdout=None, shell=True)

    installMessageEnd()


#################################################################
# Fail2ban Install
#################################################################

if fail2ban_install:
    installMessageStart("Installing Fail2Ban")

    subprocess.call("apt-get -qq -y install fail2ban", stdout=None, shell=True)

    installMessageEnd()


#################################################################
# Firewall setup
#################################################################

if firewall_setup:
    installMessageStart("Setting up firewall and port rules")

    # Enable the firewall
    subprocess.call("ufw --force enable", stdout=None, shell=True)

    # Set SSH, HTTP, and HTTPS as allowed on the system.
    # Block all other connections in and out.
    subprocess.call("ufw allow 22/tcp", stdout=None, shell=True)
    subprocess.call("ufw allow 80/tcp", stdout=None, shell=True)
    subprocess.call("ufw allow 443/tcp", stdout=None, shell=True)

    installMessageEnd()


#################################################################
# Post Install Cleanup
#################################################################

# Remove installer file
try:
    os.remove('scorpion-install.py')
except OSError:
    pass

# Print install complete message
print ""
print ""
print ""
print ""
print('Scorpion Install Complete!')
print ""