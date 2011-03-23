import serverstate
import beaconserver
import sauerserver
import settings

import asyncore

if __name__ == "__main__":
	serverState = serverstate.ServerState()
	beaconServer = beaconserver.BeaconServer(settings.hostname, settings.beaconserver_port, serverState)
	sauerServer = sauerserver.SauerServer(settings.hostname, settings.sauerserver_port, serverState)
	
	asyncore.loop()

