import beaconserver
import asyncore

if __name__ == "__main__":
	beaconServer = beaconserver.BeaconServer('', 1337)
	
	asyncore.loop()

