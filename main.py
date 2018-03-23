import mscl
import config
import statistics

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
        node_str = ""
        for n in config.basestation["nodes"]:
            node_str += str(n["address"])
            node_str += ","
        self.parent.title("Add Node")
        self.s1 = Label(self.parent, text="Node Address (Comma delimited):")
        self.s1.grid(row=0, column=0)
        self.e1 = Entry(self.parent)
        self.e1.insert(0, node_str[:-1])
        self.e1.grid(row=0, column=1)
        self.b1 = Button(self.parent, text='Add Node', command=self.addNode)
        self.b2 = Button(self.parent, text='Cancel', command=self.parent.destroy)
        self.b1.grid(row=2, column=0, sticky=W)
        self.b2.grid(row=2, column=1, sticky=W)

    def addNode(self):
        node_strings = self.e1.get().split(",")
        for n in node_strings:
            self.nodes.append(connectToNode(n, self.bs))
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

class Configuration:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.bs = None
        self.nodes = []
        self.initUI()

    def initUI(self):
        self.parent.title("BaseStation and Node Configuration")
        self.s1 = Label(self.parent, text="BaseStation:")
        self.s2 = Label(self.parent, text="Nodes:")
        self.s1.grid(row=0, column=0)
        self.s2.grid(row=1, column=0)
        self.t1 = StringVar()
        self.t2 = StringVar()
        self.v1 = Label(self.parent, text=self.t1.get())
        self.v2 = Label(self.parent, text=self.t2.get())
        self.v1.grid(row=0, column=1)
        self.v2.grid(row=1, column=1)
        self.b1 = Button(self.parent, text='Add BaseStation', command=self.promptStation).grid(row=2, column=0, sticky=W)
        self.b2 = Button(self.parent, text='Add Node', command=self.promptNode).grid(row=2, column=1, sticky=W)
        self.b3 = Button(self.parent, text='Start Sampling', command=self.closeConfig).grid(row=2, column=2, sticky=W)

    def promptStation(self):
        self.newWindow = Toplevel(self.parent)
        self.SPApp = StationPrompt(self.newWindow)

    def promptNode(self):
        self.bs = self.SPApp.getBaseStation()
        self.newWindow = Toplevel(self.parent)
        self.NApp = NodePrompt(self.newWindow, self.bs)

    def setBsText(self, string):
        self.t1.set(string)

    def setNodesText(self, string):
        self.t2.set(string)

    def getBaseStation(self):
        return self.bs

    def getNodes(self):
        return self.nodes

    def closeConfig(self):
        self.nodes = self.NApp.getNodes()
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

def main():
    print("Intializing...")
    
    conn = None
    bs = None
    network = None
    nodes = []

    root = Tk()
    app = Configuration(root)
    root.mainloop()
    bs = app.getBaseStation()
    network = mscl.SyncSamplingNetwork(bs)
    nodes = app.getNodes()
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
            data.append(getCh1(sweep))

        if len(data) > 0:
            val = statistics.median(data)
            print(val)

if __name__ == "__main__":
    main()
