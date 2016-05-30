#!/usr/bin/env python

from blog import app
import os

app.secret_key = os.urandom(24)
app.debug = True
port = int(os.environ.get('PORT', 5000))
app.run(host='127.0.0.1', port=port)
