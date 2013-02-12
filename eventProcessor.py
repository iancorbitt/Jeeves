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
# i.e securityCon.doorStatus.door1.open
#     lightingCon.lightsStatus.bed1.off
#     lightingCon.lightsStatus.door1.on

import securityController as secCon, lightingController as lightCon

def processEvent(self, event):
    print "Event received: " + event
    request = event.split('.')
    if (request[0] == "lightingCon"):
        update = lightCon.lightingCon(request)
        return update
    elif (request[0] == "securityCon"):
        update = secCon.securityCon(request)
        return update
    else:
        return "unable to process"
        print "I don't understand that Dave..."
        print request