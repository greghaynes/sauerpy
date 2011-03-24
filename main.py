#!/usr/bin/env python
# Licensed under The MIT License. See LICENSE for more details.

import serverstate
import beaconserver
import sauerserver
import settings

import logging
import asyncore

if __name__ == "__main__":
	logging.basicConfig(filename=settings.log_filename,level=settings.log_level)

	serverState = serverstate.ServerState()
	beaconServer = beaconserver.BeaconServer(settings.hostname, settings.beaconserver_port, serverState)
	sauerServer = sauerserver.SauerServer(settings.hostname, settings.sauerserver_port, serverState)
	
	asyncore.loop()

