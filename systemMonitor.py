################################################################
# Jeeves v0.1
# Ian Corbitt, 2013
#
# I'm too lazy to read into the licensing bits, so I'll just say
# that if you use my code, cool, drop me a line
################################################################

################################################################
# Request system status from all components on init
# Parse and relay status to GUI and MySQL server (for WebUI integration)

def getSystemStatus(self):
    doors = {'doors': {'door1': 'shut', 'door2': 'open', 'door3': 'shut'}}
    lights = {'lights': {'livingRoom': 'on', 'kitchen': 'on', 'bedroom1': 'off', 'bedroom2': 'off', 'bedroom3': 'on', 'bedroom4': 'off'}}
    windows = {'windows': {'window1': 'shut', 'window2': 'shut', 'window3': 'open'}}
    heating = {'heating': {'heatSetPt': 76, 'heatStatus': 'off'}}
    cooling = {'cooling': {'coolSetPt': 75, 'coolStatus': 'on'}}
    status = dict(doors.items() + windows.items() + heating.items() + cooling.items() + lights.items())
    return status