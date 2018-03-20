import mscl
import config

from tkinter import *

conn = None
bs = None
network = None
nodes = []

def connectToBaseStation(com_port, baud_rate):
    #bs = mscl.BaseStation(conn)
    print("Add base station: " + com_port + " " + baud_rate)

def connectToNode(node_addr):
    #node = mscl.WirelessNode(n["address"], bs)
    #nodes.append(node)
    print("Add node: " + node_addr)

class NodePrompt:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.initUI()

    def initUI(self):
        self.parent.title("Add Node")
        self.s1 = Label(self.parent, text="Node Address:")
        self.s1.grid(row=0, column=0)
        self.e1 = Entry(self.parent)
        self.e1.grid(row=0, column=1)
        self.b1 = Button(self.parent, text='Add Node', command=self.addNode)
        self.b2 = Button(self.parent, text='Cancel', command=self.parent.destroy)
        self.b1.grid(row=2, column=0, sticky=W)
        self.b2.grid(row=2, column=1, sticky=W)

    def addNode(self):
        connectToNode(self.e1.get())
        self.parent.destroy()
    
class StationPrompt:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.initUI()

    def initUI(self):
        self.parent.title("Add BaseStation")
        self.s1 = Label(self.parent, text="COM Port:")
        self.s2 = Label(self.parent, text="Baud Rate:")
        self.s1.grid(row=0, column=0)
        self.s2.grid(row=1, column=0)
        self.e1 = Entry(self.parent)
        self.e2 = Entry(self.parent)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.b1 = Button(self.parent, text='Add BaseStation', command=self.addBaseStation)
        self.b2 = Button(self.parent, text='Cancel', command=self.parent.destroy)
        self.b1.grid(row=2, column=0, sticky=W)
        self.b2.grid(row=2, column=1, sticky=W)

    def addBaseStation(self):
        connectToBaseStation(self.e1.get(), self.e2.get())
        self.parent.destroy()

class Configuration:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.initUI()

    def initUI(self):
        self.parent.title("BaseStation and Node Configuration")
        self.s1 = Label(self.parent, text="BaseStation:")
        self.s2 = Label(self.parent, text="Nodes:")
        self.s1.grid(row=0, column=0)
        self.s2.grid(row=1, column=0)
        self.v1 = Label(self.parent, text=bs)
        self.v2 = Label(self.parent, text=nodes)
        self.v1.grid(row=0, column=1)
        self.v2.grid(row=1, column=1)
        #t1 = Text(textvariable = v1)
        #t2 = Text(textvariable = v2)
        self.b1 = Button(self.parent, text='Add BaseStation', command=self.promptStation).grid(row=2, column=0, sticky=W)
        self.b2 = Button(self.parent, text='Add Node', command=self.promptNode).grid(row=2, column=1, sticky=W)
        self.b3 = Button(self.parent, text='Quit', command=self.parent.destroy).grid(row=2, column=2, sticky=W)

    def promptStation(self):
        self.newWindow = Toplevel(self.parent)
        self.app = StationPrompt(self.newWindow)

    def promptNode(self):
        self.newWindow = Toplevel(self.parent)
        self.app = NodePrompt(self.newWindow)

def main():
    print("Intializing...")
    
    #conn = mscl.Connection.Serial(config.basestation["com_port"], config.basestation["baud_rate"])
    #bs = mscl.BaseStation(conn)
    #network = mscl.SyncSamplingNetwork(bs)

    #for n in config.basestation["nodes"]:
    #    node = mscl.WirelessNode(n["address"], bs)
    #    nodes.append(node)
    #    network.addNode(node)

    root = Tk()
    app = Configuration(root)
    root.mainloop()

    # Read config (bs["config"])
    network.applyConfiguration()
    networks.append(network)

if __name__ == "__main__":
    main()
