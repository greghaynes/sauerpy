import beaconserver
import settings

import asyncore

if __name__ == "__main__":
	beaconServer = beaconserver.BeaconServer(settings.hostname, settings.port)
	
	asyncore.loop()

