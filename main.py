import mscl
import config

from tkinter import *

def addNodeToBasestation():
    print("testing")

def add_node():
    addNodeDisplay = Tk()
    Label(addNodeDisplay, text="Node Address").grid(row=0, column=0)
    e1 = Entry(addNodeDisplay)
    e1.grid(row=0, column=1)
    Button(addNodeDisplay, text='Add Node', command=addNodeToBasestation).grid(row=1)
    mainloop()

def displayNodes(nodes):
    nodeDisplay = Tk()
    nodeStr = config.basestation["nodes"]

    e1 = Text(nodeDisplay,height=2)
    e1.insert(INSERT, nodeStr)
    e1.pack()
    e1.grid(row=0, column=0)
    
    Button(nodeDisplay, text='Add Node', command=add_node).grid(row=1, column=0, sticky=W, pady=4)

    mainloop()


def displayPrompt(bs,nodes):
    if bs is None:
        promptStation()
    else:
        displayNodes(nodes)

def main():
    print("Intializing...")

    networks = []
    nodes_master = []
    
    conn = mscl.Connection.Serial(config.basestation["com_port"], config.basestation["baud_rate"])
    bs = mscl.BaseStation(conn)
    network = mscl.SyncSamplingNetwork(bs)

    nodes = []
    for n in config.basestation["nodes"]:
        node = mscl.WirelessNode(n["address"], bs)
        nodes.append(node)
        network.addNode(node)
    nodes_master.append(nodes)

    displayPrompt(bs,nodes)

    # Read config (bs["config"])
    network.applyConfiguration()
    networks.append(network)

if __name__ == "__main__":
    main()
