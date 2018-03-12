import mscl

def printNodeCurrentConfig(node):
    print("Configuration of node: " + str(config.NODE_ADDR))
    print("# of Triggers:", node.getNumDatalogSessions())
    print("User Inactivity Timeout:", node.getInactivityTimeout(), "seconds")
    print("Total active channels:", node.getActiveChannels().count())
    print("# of sweeps:", node.getNumSweeps())

def printNetworkInfo(network):
    print("Network info: ")
    print("Network OK: ", network.ok())
    print("Percent of Bandwidth: ", network.percentBandwidth())
    print("Lossless Enabled: ", network.lossless())

def printSweepData(sweep):
    packet = {"nodeAddress": sweep.nodeAddress(),
            "timestamp": sweep.timestamp(),
            "tick": sweep.tick(),
            "sampleRate": sweep.sampleRate().prettyStr(),
            "baseRSSI": sweep.baseRssi(),
            "nodeRSSI": sweep.nodeRssi()}

    data = []
    for dataPoint in sweep.data():
        data.append(dataPoint.as_float())

    print(data)

def cleanUpNode(nodes):
    print("Cleaning up..")
    for node in nodes:
        print("Setting node " + str(config.NODE_ADDR) + " to idle")
        status = node.setToIdle()
        while not status.complete(300):
            print(".")
        result = status.result()
        if result == mscl.SetToIdleStatus.setToIdleResult_success:
            print("Set node to idle")
        elif result == mscl.SetToIdleStatus.canceled:
            print("Setting node to idle cancelled")
        else:
            print("Setting to idle failed")
