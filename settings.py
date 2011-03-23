# Licensed under The MIT License. See LICENSE for more details.
# Configuration file for the server

# Just ignore these import lines
import mastermodes
import gamemodes

# Server description
server_desc = 'A sauerpy server'

# Server hostname or IP
hostname = ''

# Server port
port = 1337

# Master mode
master_mode = mastermodes.OPEN

# Maximum number of clients
max_clients = 16

# Game mode
game_mode = gamemodes.FFA

# First map
start_map = 'complex'

# *****************************************************************
# Dont touch settings below here unless you know what youre doing |
# *****************************************************************
beaconserver_port = port + 1
sauerserver_port = port

protocol_version = 258

match_length = 600 # In seconds

