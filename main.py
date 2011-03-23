import gamestate
import beaconserver
import sauerserver
import settings

import asyncore

if __name__ == "__main__":
	gameState = gamestate.GameState()
	beaconServer = beaconserver.BeaconServer(settings.hostname, settings.port, gameState)
	sauerServer = sauerserver.SauerServer(settings.hostname, settings.sauerserver_port, gameState)
	
	asyncore.loop()

