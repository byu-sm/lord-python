import mscl
import config
import statistics
import thingworx

from tkinter import *

def connectToBaseStation(com_port, baud_rate):
    conn = mscl.Connection.Serial(com_port, int(baud_rate))
    bs = mscl.BaseStation(conn)
    print("Add base station: " + com_port + " " + baud_rate)
    return bs

def connectToNode(node_addr, bs):
    node = mscl.WirelessNode(int(node_addr), bs)
    print("Add node: " + node_addr)
    return node

class NodePrompt:
    def __init__(self, parent, bs):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.bs = bs
        self.nodes = []
        self.initUI()

    def initUI(self):
        node_addr_str = ""
        node_type_str = ""
        for n in config.basestation["nodes"]:
            node_addr_str += str(n["address"])
            node_addr_str += ","
            node_type_str += str(n["type"])
            node_type_str += ","
        self.parent.title("Add Node")
        self.s1 = Label(self.parent, text="Node Address (Comma delimited):")
        self.s1.grid(row=0, column=0)
        self.e1 = Entry(self.parent)
        self.e1.insert(0, node_addr_str[:-1])
        self.e1.grid(row=0, column=1)
        self.s2 = Label(self.parent, text="Node Types (Comma delimited):")
        self.s2.grid(row=1, column=0)
        self.e2 = Entry(self.parent)
        self.e2.insert(0, node_type_str[:-1])
        self.e2.grid(row=1, column=1)
        self.b1 = Button(self.parent, text='Add Node', command=self.addNode)
        self.b2 = Button(self.parent, text='Cancel', command=self.parent.destroy)
        self.b1.grid(row=2, column=0, sticky=W)
        self.b2.grid(row=2, column=1, sticky=W)

    def addNode(self):
        node_addrs = self.e1.get().split(",")
        node_types = self.e2.get().split(",")
        len_addr = len(node_addrs)
        len_types = len(node_types)
        if len_addr == len_types:
            for i in range(0,len_addr-1):
                self.nodes.append({"address": node_addrs[i], "type": node_types[i]})
        self.parent.destroy()

    def getNodes(self):
        return self.nodes
    
class StationPrompt:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.conn = None
        self.bs = None
        self.initUI()

    def initUI(self):
        self.parent.title("Add BaseStation")
        self.s1 = Label(self.parent, text="COM Port:")
        self.s2 = Label(self.parent, text="Baud Rate:")
        self.s1.grid(row=0, column=0)
        self.s2.grid(row=1, column=0)
        self.e1 = Entry(self.parent)
        self.e2 = Entry(self.parent)
        self.e1.insert(0, config.basestation["com_port"])
        self.e2.insert(0, config.basestation["baud_rate"])
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.b1 = Button(self.parent, text='Add BaseStation', command=self.addBaseStation)
        self.b2 = Button(self.parent, text='Cancel', command=self.parent.destroy)
        self.b1.grid(row=2, column=0, sticky=W)
        self.b2.grid(row=2, column=1, sticky=W)

    def addBaseStation(self):
        self.bs = connectToBaseStation(self.e1.get(), self.e2.get())
        self.parent.destroy()

    def getBaseStation(self):
        return self.bs

class Tw_config:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.bs = None
        self.nodes = []
        self.initUI()

    def initUI(self):
        self.parent.title("ThingWorx Host Configuration")
        self.s1 = Label(self.parent, text="Server IP:")
        self.s2 = Label(self.parent, text="APP_Key:")
        self.s3 = Label(self.parent, text="Username:")
        self.s4 = Label(self.parent, text="Password:")
        self.s1.grid(row=0, column=0)
        self.s2.grid(row=1, column=0)
        self.s3.grid(row=2, column=0)
        self.s4.grid(row=3, column=0)
        self.e1 = Entry(self.parent)
        self.e2 = Entry(self.parent)
        self.e3 = Entry(self.parent)
        self.e4 = Entry(self.parent)
        self.e1.insert(0, config.THINGWORX_HOST)
        self.e2.insert(0, config.APP_KEY)
        self.e3.insert(0, config.HTTP_USERNAME)
        self.e4.insert(0, config.HTTP_PASSWORD)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        self.b1 = Button(self.parent, text='Configure Basestation', command=self.promptStation).grid(row=4, column=0, sticky=W)

    def promptStation(self):
        self.closeConfig()

    def closeConfig(self):
        self.parent.destroy()

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

def printSweepData(sweep):
    data = []
    for dataPoint in sweep.data():
        data.append(dataPoint.as_float())

    print(data)

def getDataTempSensor(sweep, data):
    data.append(getCh1(sweep))

    if len(data) > 0:
        val = statistics.median(data)
        print(val)
        print(thingworx.putDataToThing("LordThing", "temp", val))

def getDataForceSensor(sweep):
    print(sweep.data())
    return

def updateConfig():
    #Update Config Here
    return None

def main():
    print("Intializing...")
    
    conn = None
    bs = None
    network = None
    nodes = []

    root = Tk()
    app = Tw_config(root)
    root.mainloop()

    root = Tk()
    app = StationPrompt(root)
    root.mainloop()
    bs = app.getBaseStation()
    print(bs)

    root = Tk()
    app = NodePrompt(root, bs)
    root.mainloop()
    nodes_temp = app.getNodes()
    for n in nodes_temp:
        nodes.append(connectToNode(n["address"], bs))
    print(nodes)

    #updateConfig(bs, nodes)

    if bs:
        network = mscl.SyncSamplingNetwork(bs)
        if len(nodes) > 0:
            print(nodes)
            for node in nodes:
                network.addNode(node)

            # Read config (bs["config"])
            network.applyConfiguration()
            network.startSampling()

            print("Parsing the data (while True loop)")
            while True:
                # get all data sweeps (timeout 500ms)
                sweeps = bs.getData(1000)

                data = []
                for sweep in sweeps:
                    #printSweepData(sweep)
                    n_addr = sweep.nodeAddress()
                    n_type = None
                    for n in nodes_temp:
                        if n["address"] == n_addr:
                            n_type = n["type"]
                        else:
                            n_type = "force"
                    if n_type == "temp":
                        getDataTempSensor(sweep, data)
                    elif n_type == "force":
                        getDataForceSensor(sweep)

if __name__ == "__main__":
    main()
