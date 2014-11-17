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

## Allow modules to be imported from the libraries directory.
import sys
sys.path.append('./libraries')

## Import modules for use
import os
import platform

## Maybe someday I will create an interface using blessings...
#from blessings import Terminal

os.environ["AWS_CREDENTIAL_FILE"] = ".awskeys"

## Allow the script to move forward regardless of compatibility issues.
devmode = True

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

## Uncheck to see distribution information.
#print platform.dist()
#print platform.system()

## Create connection to AWS S3
#s3conn = boto.connect_s3()

## Get all available buckets.
#buckets = s3conn.get_all_buckets()

## List the buckets.
#for bucket in buckets:
#    print bucket.name