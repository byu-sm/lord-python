import mscl
import lord
import thingworx
import config

import statistics
from tkinter import *

class StationConfig:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.com_port = None
        self.baud_rate = None
        self.initUI()

    def initUI(self):
        self.parent.title("Add BaseStation")
        Label(self.parent, text="COM Port:").grid(row=0, column=0)
        Label(self.parent, text="Baud Rate:").grid(row=1, column=0)
        
        self.e1 = Entry(self.parent)
        self.e2 = Entry(self.parent)
        self.e1.insert(0, config.basestation["com_port"])
        self.e2.insert(0, config.basestation["baud_rate"])
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        
        Button(self.parent, text='Add BaseStation', command=self.setBaseStation).grid(row=2, column=0, sticky=W)

    def setBaseStation(self):
        self.com_port = self.e1.get()
        self.baud_rate = self.e2.get()
        self.parent.destroy()

    def getComPort(self):
        return self.com_port

    def getBaudRate(self):
        return self.baud_rate

class NodeConfig:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.nodes = []
        self.node_addr_str = ""
        self.node_type_str = ""
        for n in config.basestation["nodes"]:
            self.node_addr_str += str(n["address"])
            self.node_addr_str += ","
            self.node_type_str += str(n["type"])
            self.node_type_str += ","
        self.initUI()

    def initUI(self):
        self.parent.title("Add Node")
        Label(self.parent, text="Node Address (Comma delimited):").grid(row=0, column=0)
        Label(self.parent, text="Node Types (Comma delimited):").grid(row=1, column=0)
        
        self.e1 = Entry(self.parent)
        self.e2 = Entry(self.parent)
        self.e1.insert(0, self.node_addr_str[:-1])
        self.e2.insert(0, self.node_type_str[:-1])
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        
        Button(self.parent, text='Add Node', command=self.setNodes).grid(row=2, column=0, sticky=W)

    def setNodes(self):
        self.node_addrs = self.e1.get().split(",")
        self.node_types = self.e2.get().split(",")
        len_addr = len(self.node_addrs)
        len_types = len(self.node_types)
        if len_addr == len_types:
            for i in range(0,len_addr):
                self.nodes.append({"address": self.node_addrs[i], "type": self.node_types[i]})
        self.parent.destroy()

    def getNodes(self):
        return self.nodes

class ThingWorxConfig:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.serverIp = None
        self.appKey = None
        self.username = None
        self.password = None
        self.initUI()

    def initUI(self):
        self.parent.title("ThingWorx Host Configuration")
        Label(self.parent, text="Server IP:").grid(row=0, column=0)
        Label(self.parent, text="APP_Key:").grid(row=1, column=0)
        Label(self.parent, text="Username:").grid(row=2, column=0)
        Label(self.parent, text="Password:").grid(row=3, column=0)
        
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
        
        Button(self.parent, text='Configure Basestation', command=self.setConfig).grid(row=4, column=0, sticky=W)

    def setConfig(self):
        self.serverIp = self.e1.get()
        self.appKey = self.e1.get()
        self.username = self.e1.get()
        self.password = self.e1.get()
        self.closeConfig()

    def closeConfig(self):
        self.parent.destroy()

    def closeConfig(self):
        self.parent.destroy()

    def getConfig(self):
        config = {
            "server_ip": self.serverIp,
            "app_key": self.appKey,
            "username": self.username,
            "password": self.password
            }
        return config

def main():
    print("Initializing connection to Lord Sensors and ThingWorx")

    win1 = Tk()
    app1 = StationConfig(win1)
    win1.mainloop()
    com_port = app1.getComPort()
    baud_rate = app1.getBaudRate()

    win2 = Tk()
    app2 = NodeConfig(win2)
    win2.mainloop()
    nodes = app2.getNodes()
    print(nodes)

    win3 = Tk()
    app3 = ThingWorxConfig(win3)
    win3.mainloop()
    tw_config = app3.getConfig()

    #updateConfig(bs, nodes, tw_config)
    
    bs = lord.connectToBaseStation(com_port, baud_rate)
    if bs:
        network = mscl.SyncSamplingNetwork(bs)
        if len(nodes) > 0:
            for node in nodes:
                network.addNode(lord.connectToNode(node["address"], bs))

        network.applyConfiguration()
        network.startSampling()

        while True:
            TIMEOUT = 1000 # 500ms
            val = lord.parseData(bs.getData(TIMEOUT))
            if val is not None:
                print(val)
                print(thingworx.putDataToThing("LordThing", "temp", val))

if __name__ == "__main__":
    main()
