################################################################
# Jeeves v0.1
# Ian Corbitt, 2013
#
# I'm too lazy to read into the licensing bits, so I'll just say
# that if you use my code, cool, drop me a line
################################################################

################################################################
# Event format
#
# <station_id>.<request_type>.<event>.<argument(s)>
#
# i.e relayCon.doorStatus.door1.open
#     lightingCon.lightsStatus.bed1.off
#     lightingCon.lightsStatus.door1.on

def processEvent(event):
    print "Event received: " + event