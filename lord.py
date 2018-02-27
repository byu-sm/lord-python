import mscl
import requests
import time
import config

print("Setting up basestation and node configuration")
print("Using MSCL library version: " + mscl.LibVersion.asString())

def sendDataToThingWorx(thingName, key, data):
    url = "http://" + config.THINGWORX_HOST + "/Thingworx/Things/" + thingName + "/Properties/" + key

    querystring = {"appKey": config.APP_KEY}

    payload = str("{\"" + key + "\":" + str(data) + "}")
    headers = {
        'Content-Type': "application/json",
        'Authorization': config.HTTP_BASIC_AUTH,
        'Cache-Control': "no-cache",
        'Postman-Token': "d8280d1d-64a9-da31-ed2b-0948a24a6966"
        }

    response = requests.request("PUT", url, data=payload, headers=headers, params=querystring)
    #print(response.text)

def getCurrentConfig(node):
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

    data = {}
    for dataPoint in sweep.data():
        data[dataPoint.channelName()] = dataPoint.as_float()

    packet["data"] = data

    print(packet)
    print(str(packet["data"]["ch1"]) + " : " + str(packet["data"]["ch7"]))
    sendDataToThingWorx("LordThing", "temp", packet["data"]["ch1"])


def cleanUp(node):
    print("Cleaning up..")
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

try:
    print("Connection basestation on " + config.COM_PORT)
    conn = mscl.Connection.Serial(config.COM_PORT, config.BS_BAUD)
    bs = mscl.BaseStation(conn)

    if (bs.ping()):
        print("Connected to BaseStation succesfully")
    else:
        print("Failed to ping the created BaseStation")
        exit()

    node = mscl.WirelessNode(config.NODE_ADDR, bs)
    if (node.ping()):
        print("Connected to node at address " + str(config.NODE_ADDR) + " succesfully")
    else:
        print("Failed to ping node " + str(config.NODE_ADDR))

    getCurrentConfig(node)

    print("Creating a synchronized network for sampling the node(s)")
    network = mscl.SyncSamplingNetwork(bs)

    print("Adding node " + str(config.NODE_ADDR) + " to network")
    network.addNode(node)
    printNetworkInfo(network)

    print("Applying network configuration to nodes in network..")    
    network.applyConfiguration()

    print("Starting sampling the network..")
    network.startSampling()

    print("Parsing the data (while True loop)")
    while True:
        # get all data sweeps (timeout 500ms)
        sweeps = bs.getData(500)

        for sweep in sweeps:
            printSweepData(sweep)
        time.sleep(1)
except KeyboardInterrupt:
    cleanUp(node)

except Exception as e:
    print("Error: " + e)
