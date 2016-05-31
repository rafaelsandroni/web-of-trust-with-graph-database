#!/usr/bin/python
import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
#site.addsitedir('/home/rafael/Python/MyReputation/myprojectenv/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
#sys.path.append('/home/rafael/Python/MyReputation')

# Activate your virtual env
activate_this="/home/rafael/Python/MyReputation/myprojectenv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, "/home/rafael/Python/MyReputation")

from run import app as application
