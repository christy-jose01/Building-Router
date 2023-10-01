from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):

    # create all of the hosts
    h10 = self.addHost('h10', mac='00:00:00:00:00:01', ip = '10.1.1.10/24', defaultRoute="h10-eth0")
    h20 = self.addHost('h20', mac='00:00:00:00:00:02', ip = '10.1.2.20/24', defaultRoute="h20-eth0")
    h30 = self.addHost('h30', mac='00:00:00:00:00:03', ip = '10.1.3.30/24', defaultRoute="h30-eth0")
    h40 = self.addHost('h40', mac='00:00:00:00:00:04', ip = '10.1.4.40/24', defaultRoute="h40-eth0")

    h50 = self.addHost('h50', mac='00:00:00:00:00:05', ip = '10.2.5.50/24', defaultRoute="h50-eth0")
    h60 = self.addHost('h60', mac='00:00:00:00:00:06', ip = '10.2.6.60/24', defaultRoute="h60-eth0")
    h70 = self.addHost('h70', mac='00:00:00:00:00:07', ip = '10.2.7.70/24', defaultRoute="h70-eth0")
    h80 = self.addHost('h80', mac='00:00:00:00:00:08', ip = '10.2.8.80/24', defaultRoute="h80-eth0")

    h_trust = self.addHost('h_trust', mac='00:00:00:00:00:09', ip = '108.24.31.112/24', defaultRoute="h_trust-eth0")
    h_untrust = self.addHost('h_untrust', mac='00:00:00:00:00:10', ip = '106.44.82.103/24', defaultRoute="h_untrust-eth0")
    h_server = self.addHost('h_server', mac='00:00:00:00:00:11', ip = '10.3.9.90/24', defaultRoute="h_server-eth0")

    # create the switches
    s1 = self.addSwitch('s1')
    s2 = self.addSwitch('s2')
    # core switch name = s3
    s3 = self.addSwitch('s3')
    # data center switch name = s4
    s4 = self.addSwitch('s4')

    s5 = self.addSwitch('s5')
    s6 = self.addSwitch('s6')
    

    # --------------------connections-------------------------------------
    # Floor 1
      # for switch 1
    # self.addLink(h10, s1, port1 = 0, port2 = 20)
    self.addLink(s1, h10, port1 = 20, port2 = 0)
    # self.addLink(h20, s1, port1 = 0, port2 = 21)
    self.addLink(s1, h20, port1 = 21, port2 = 0)
      # for switch 2
    # self.addLink(h30, s2, port1 = 0, port2 = 22)
    # self.addLink(h40, s2, port1 = 0, port2 = 23)
    self.addLink(s2, h30, port1 = 22, port2 = 0)
    self.addLink(s2, h40, port1 = 23, port2 = 0)

    # Floor 2
      # for switch 5
    # self.addLink(h50, s5, port1 = 0, port2 = 24)
    # self.addLink(h60, s5, port1 = 0, port2 = 25)
    self.addLink(s5, h50, port1 = 24, port2 = 0)
    self.addLink(s5, h60, port1 = 25, port2 = 0)
      # for switch 6
    # self.addLink(h70, s6, port1 = 0, port2 = 26)
    # self.addLink(h80, s6, port1 = 0, port2 = 27)
    self.addLink(s6, h70, port1 = 26, port2 = 0)
    self.addLink(s6, h80, port1 = 27, port2 = 0)

    # data center
    # self.addLink(h_server, s4, port1 = 0, port2 = 10)
    self.addLink(s4, h_server, port1 = 10, port2 = 0)

    # Core
      # Floor 1
    self.addLink(s1, s3, port1 = 11, port2 = 1)
    self.addLink(s2, s3, port1 = 12, port2 = 2)
      # Floor 2
    self.addLink(s5, s3, port1 = 13, port2 = 3)
    self.addLink(s6, s3, port1 = 14, port2 = 4)
      # untrusted host
    # self.addLink(h_untrust, s3, port1 = 0, port2 = 5)
    self.addLink(s3, h_untrust, port1 = 5, port2 = 0)
      # trusted host
    # self.addLink(h_trust, s3, port1 = 0, port2 = 6)
    self.addLink(s3, h_trust, port1 = 6, port2 = 0)
      # data center
    self.addLink(s4, s3, port1 = 17, port2 = 7)


def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()