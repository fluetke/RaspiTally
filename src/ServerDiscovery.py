'''
Created on 06.02.2015

@author: Florian
'''
from PyQt4.Qt import QUdpSocket

class ServerAnnouncer(QObject):
    '''
    this acts as an announcer for a server on the network,
    it emits udp packets which contain the address of the server and type of service  
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(ServerAnnouncer, self).__init__(parent)
        
    def run():
        socket = QUdpSocket(self)
        socket.bind(QHostAddress.Broadcast, 0)
        socket.setSocketOption()
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket
        TALLY_IP = gethostbyname(gethostname()) #get our IP. Be careful if you have multiple network interfaces or IPs
        print(TALLY_IP)
        data = ANNOUNCE_TOKEN+TALLY_IP+":"+str(TALLY_PORT)
        while RUN_ANNOUNCER:
            #print(type(data))
            s.sendto(bytes(data, 'UTF-8'), ('<broadcast>', PORT))
            print("sent tally-service announcement")
            sleep(5)
        