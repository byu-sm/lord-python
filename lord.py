import mscl
import statistics


def getCh1(sweep):
    data = {}
    for dataPoint in sweep.data():
        data[dataPoint.channelName()] = dataPoint.as_float()
    return data["ch1"]


def getCh2(sweep):
    data = {}
    for dataPoint in sweep.data():
        data[dataPoint.channelName()] = dataPoint.as_float()
    return data["ch2"]


def parseData(sweeps):
    data = []
    for sweep in sweeps:
        data.append(getCh1(sweep))

    if len(data) > 0:
        return statistics.median(data)
    else:
        return None


def connectToBaseStation(com_port, baud_rate):
    conn = mscl.Connection.Serial(com_port, int(baud_rate))
    bs = mscl.BaseStation(conn)
    print("Connect base station: " + com_port + " " + baud_rate)
    return bs


def connectToNode(node_addr, bs):
    node = mscl.WirelessNode(int(node_addr), bs)
    print("Connect node: " + node_addr)
    return node

class TempNode:
    def __init__(self, node_addr, node_type):
        self.node_addr = node_addr
        self.node_type = node_type
        self.node = None

    def connectNode(self, bs):
        self.node = mscl.WirelessNode(int(self.node_addr), bs)
        print("Connect node: " + self.node_addr)
        return self.node

    def getNodeType(self):
        return self.node_type

    def cleanUp(self):
        print("Cleaning up node: " + self.node_addr)
        status = self.node.setToIdle()
        while not status.complete(300):
            print(".")
        result = status.result()
        if result == mscl.SetToIdleStatus.setToIdleResult_success:
            print("Set " + self.node_addr + " to idle")
        elif result == mscl.SetToIdleStatus.canceled:
            print("Setting " + self.node_addr + " to idle cancelled")
        else:
            print("Setting " + self.node_addr + " to idle failed")

class ForceNode:
    def __init__(self, node_addr, node_type):
        self.node_addr = node_addr
        self.node_type = node_type
        self.node = None

    def connectNode(self, bs):
        self.node = mscl.WirelessNode(int(self.node_addr), bs)
        print("Connect node: " + self.node_addr)
        return self.node

    def getNodeType(self):
        return self.node_type

    def cleanUp(self):
        print("Cleaning up node: " + self.node_addr)
        status = self.node.setToIdle()
        while not status.complete(300):
            print(".")
        result = status.result()
        if result == mscl.SetToIdleStatus.setToIdleResult_success:
            print("Set " + self.node_addr + " to idle")
        elif result == mscl.SetToIdleStatus.canceled:
            print("Setting " + self.node_addr + " to idle cancelled")
        else:
            print("Setting " + self.node_addr + " to idle failed")
