#!/usr/bin/env python

import os

from .daemons import ToggleDaemon

d = ToggleDaemon(os.environ)
d.run_forever()
