import Lord/mscl
import config

def main():
    print("Intializing...")

    # Use this space for GUI code and gathering information about sensors to connect
    
    stations = []
    networks = []
    nodes_master = []
    for bs in config.basestations:
        conn = mscl.Connection.Serial(bs["com_port"], bs["baud_rate"])
        station = mscl.BaseStation(conn)
        stations.add(station)
        network = mscl.SyncSamplingNetwork(station)

        nodes = []
        for n in config.basestations["nodes"]:
            node = mscl.WirelessNode(n["address"], station)
            nodes.add(node)
            network.addNode(node)
        nodes_master.add(nodes)

        # Read config (bs["config"])
        network.applyConfiguration()
        networks.add(network)

if __name__ == "__main__":
    main()
