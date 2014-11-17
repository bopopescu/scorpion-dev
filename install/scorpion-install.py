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

import os
import argparse

try: input = raw_input
except NameError: pass

print('''
    Installing Scorpion Server Manager
                               _               _
   ______________  _________  (_)___  ____    (_)___
  / ___/ ___/ __ \/ ___/ __ \/ / __ \/ __ \  / / __ \\
 (__  ) /__/ /_/ / /  / /_/ / / /_/ / / / / / / /_/ /
/____/\___/\____/_/  / .___/_/\____/_/ /_(_)_/\____/
                    /_/
''')

parser = argparse.ArgumentParser(description='AWS Credentials for saving and restoring backups.')
parser.add_argument('--aws-access-key-id')
parser.add_argument('--aws-secret-access-key')

args = parser.parse_args()

AWS_AKID = args.aws_access_key_id
AWS_SAK = args.aws_secret_access_key

if not AWS_AKID:
    AWS_AKID = input('Enter your AWS Access Key ID: ')

if not AWS_SAK:
    AWS_SAK = input('Enter your AWS Secret Access Key: ')

print AWS_AKID
print AWS_SAK

## Kick off another script
#os.system('python hello.py')

print('Complete')

try:
    os.remove('scorpion-install.py')
except OSError:
    pass