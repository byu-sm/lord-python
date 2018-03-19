import mscl
import config

from tkinter import *

def displayNodes(nodes):
    nodeDisplay = Tk()
    Label(nodeDisplay, text=nodes).grid(row=0)
    e1 = Entry(nodeDisplay)
    e1.grid(row=0, column=0)

    Button(nodeDisplay(), text='Add Node', command=add_node).grid(row=1, column=0, sticky=W, pady=4)
    Button(nodeDisplay(), text='Quit', command=nodeDisplay.quit).grid(row=1, column=1, sticky=W, pady=4)

def displayPrompt(bs,nodes):
    if bs == null:
        promptStation()
    else:
        displayNodes(nodes)

def main():
    print("Intializing...")

    networks = []
    nodes_master = []
    
    conn = mscl.Connection.Serial(config.basestation["com_port"], basestation["baud_rate"])
    bs = mscl.BaseStation(conn)
    network = mscl.SyncSamplingNetwork(bs)

    nodes = []
    for n in config.basestations["nodes"]:
        node = mscl.WirelessNode(n["address"], bs)
        nodes.add(node)
        network.addNode(node)
    nodes_master.add(nodes)

    displayPrompt(bs,nodes)

    # Read config (bs["config"])
    network.applyConfiguration()
    networks.add(network)

if __name__ == "__main__":
    main()
