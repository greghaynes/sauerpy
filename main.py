import beaconserver
import sauerserver
import settings

import asyncore

if __name__ == "__main__":
	beaconServer = beaconserver.BeaconServer(settings.hostname, settings.port)
	sauerServer = sauerserver.SauerServer(settings.hostname, settings.sauerserver_port)
	
	asyncore.loop()

