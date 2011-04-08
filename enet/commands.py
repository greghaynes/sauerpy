NONE = 0
ACKNOWLEDGE = 1
CONNECT = 2
CONNECT_VERIFY = 3
DISCONNECT = 4
PING = 5
SEND_RELIABLE = 6
SEND_UNRELIABLE = 7
SEND_FRAGMENT = 8
SEND_UNSEQUENCED = 9
BANDWIDTH_LIMIT = 10
THROTTLE_CONFIGURE = 11
COUNT = 12

FLAG_ACKNOWLEDGE = 1<<7
FLAG_UNSEQUENCED = 1<<6

HEADER_FLAG_COMPRESSED = 1 << 14
HEADER_FLAG_TIMESTAMP = 1 << 15
HEADER_FLAG_MASK = HEADER_FLAG_COMPRESSED | HEADER_FLAG_TIMESTAMP
HEADER_SESSION_MASK = 3 << 12
HEADER_SESSION_SHIFT = 12
