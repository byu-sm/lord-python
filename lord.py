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