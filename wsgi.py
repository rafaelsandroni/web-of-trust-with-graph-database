#!/usr/bin/python
import os
import sys
import site

# virtual env runing on Apache
activate_this="/home/rafael/Python/MyReputation/myprojectenv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, "/home/rafael/Python/MyReputation")

from run import app as application
