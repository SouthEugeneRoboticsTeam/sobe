# Communicates with RoboRIO
import networktables

net = None

def net_init(ip):
    global net
    try:
        net = networktables.NetworkTables.initialize(server=ip)
    except:
        return (False,"Could not connect to the RoboRIO on IP:" + ip)
    return (True,"")

def send_to_network(value):
    try:
        table = net.getTable('Vision')
        table.putNumber("x_offset",value)
    except:
        return (False,"Could not update the NetworkTable")
    return (True,"")