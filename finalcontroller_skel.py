from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):

  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)


  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 3:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.
    def drop(packet, packet_in):
      print("dropping")
      msg = of.ofp_flow_mod()
      # installing the role to the switch
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 30
      msg.hard_timeout = 30
      msg.data = packet_in
      self.connection.send(msg)

    def flood (packet, packet_in, port_num):
      print("flooding")
      msg = of.ofp_flow_mod()
      # installs the role to the switch
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 30
      msg.hard_timeout = 30
      msg.actions.append(of.ofp_action_output(port = port_num))
      msg.data = packet_in
      self.connection.send(msg)

    #  the actual filtering
    arp = packet.find('arp')
    ipv4 = packet.find('ipv4')
    icmp = packet.find('icmp')

    # from info:
    # port_on_switch: sender's port
    # switch_id: sender's switch

    # dest info:
    # # dest_ip: receiver's ip address
    # dest_ip = str(ipv4.dstip)

    # dict of "ip address" : port_num (pov of core switch)
    addy = {
      "10.1.1.10": 1, #h10 floor1
      "10.1.2.20": 1, #h20 floor1
      "10.1.3.30": 2, #h30 floor1
      "10.1.4.40": 2, #h40 floor1
      "10.2.5.50": 3, #h50 floor2
      "10.2.6.60": 3, #h60 floor2
      "10.2.7.70": 4, #h70 floor2
      "10.2.8.80": 4, #h80 floor2
      "106.44.82.103": 5, #h_untrust 
      "108.24.31.112": 6, #h_trust
      "10.3.9.90": 7 #h_server
    }

    # if arp:
    #   print("it is ARP duhhh")
    #   flood(packet, packet_in, of.OFPP_FLOOD)

    if arp:
      msg = of.ofp_flow_mod()
      # installs the role to the switch
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 30
      msg.hard_timeout = 30
      msg.data = packet_in
      msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      self.connection.send(msg)
      print("finished arping")

    if ipv4 is not None:
      if icmp is not None:
        # dest_ip: receiver's ip address
        dest_ip = str(ipv4.dstip)
        # SWITCH 1
        if switch_id == 1:
          # check dest_ip and forward it
          # from core
          if dest_ip == "10.1.1.10":
            flood(packet, packet_in, 20) # to h10
          elif dest_ip == "10.1.2.20":
            flood(packet, packet_in, 21) # to h20
          else:
            flood(packet, packet_in, 11) # to s3/core
          

        # SWITCH 2
        elif switch_id == 2:
          # check dest_ip and forward it
          if dest_ip == "10.1.3.30":
            flood(packet, packet_in, 22) # to h30
          elif dest_ip == "10.1.4.40":
            flood(packet, packet_in, 23) # to h40
          else:
            flood(packet, packet_in, 12) # to s3/core
          
        # SWITCH 3/ CORE
        elif switch_id == 3: 

          # The firewall part
          if port_on_switch == 5: # from h_untrust
            if dest_ip == "10.1.1.10":
              drop(packet, packet_in) # drop h10
            if dest_ip == "10.1.2.20":
              drop(packet, packet_in) # drop h20
            if dest_ip == "10.1.3.30":
              drop(packet, packet_in) # drop h30
            if dest_ip == "10.1.4.40":
              drop(packet, packet_in) # drop h40
            if dest_ip == "10.2.5.50":
              drop(packet, packet_in) # drop h50
            if dest_ip == "10.2.6.60":
              drop(packet, packet_in) # drop h60
            if dest_ip == "10.2.7.70":
              drop(packet, packet_in) # drop h70
            if dest_ip == "10.2.8.80":
              drop(packet, packet_in) # drop h80
            if dest_ip == "108.24.31.112":
              flood(packet, packet_in, addy["108.24.31.112"]) #h_trust
            if dest_ip == "10.3.9.90":
              drop(packet, packet_in) # drop h_server
          
          if port_on_switch == 6: # from h_trust
            if dest_ip == "10.1.1.10":
              flood(packet, packet_in, addy["10.1.1.10"]) #h10
            if dest_ip == "10.1.2.20":
              flood(packet, packet_in, addy["10.1.2.20"]) #h20
            if dest_ip == "10.1.3.30":
              flood(packet, packet_in, addy["10.1.3.30"]) #h30
            if dest_ip == "10.1.4.40":
              flood(packet, packet_in, addy["10.1.4.40"]) #h40
            if dest_ip == "10.2.5.50":
              drop(packet, packet_in) # drop h50
            if dest_ip == "10.2.6.60":
              drop(packet, packet_in) # drop h60
            if dest_ip == "10.2.7.70":
              drop(packet, packet_in) # drop h70
            if dest_ip == "10.2.8.80":
              drop(packet, packet_in) # drop h80
            if dest_ip == "106.44.82.103":
              flood(packet, packet_in, addy["106.44.82.103"]) #h_untrust
            if dest_ip == "10.3.9.90":
              drop(packet, packet_in) # drop h_server
          
          if port_on_switch == 1 or port_on_switch == 2: # from h10-h40
            if dest_ip == "10.1.1.10":
              flood(packet, packet_in, addy["10.1.1.10"]) #h10
            if dest_ip == "10.1.2.20":
              flood(packet, packet_in, addy["10.1.2.20"]) #h20
            if dest_ip == "10.1.3.30":
              flood(packet, packet_in, addy["10.1.3.30"]) #h30
            if dest_ip == "10.1.4.40":
              flood(packet, packet_in, addy["10.1.4.40"]) #h40
            if dest_ip == "10.2.5.50":
              drop(packet, packet_in) # drop h50
            if dest_ip == "10.2.6.60":
              drop(packet, packet_in) # drop h60
            if dest_ip == "10.2.7.70":
              drop(packet, packet_in) # drop h70
            if dest_ip == "10.2.8.80":
              drop(packet, packet_in) # drop h80
            if dest_ip == "108.24.31.112":
              flood(packet, packet_in, addy["108.24.31.112"]) #h_trust
            if dest_ip == "106.44.82.103":
              flood(packet, packet_in, addy["106.44.82.103"]) #h_untrust
            if dest_ip == "10.3.9.90":
              flood(packet, packet_in, addy["10.3.9.90"]) #h_server
          
          if port_on_switch == 3 or port_on_switch == 4: # from h50-h80
            if dest_ip == "10.1.1.10":
              drop(packet, packet_in) # drop h10
            if dest_ip == "10.1.2.20":
              drop(packet, packet_in) # drop h20
            if dest_ip == "10.1.3.30":
              drop(packet, packet_in) # drop h30
            if dest_ip == "10.1.4.40":
              drop(packet, packet_in) # drop h40
            if dest_ip == "10.2.5.50":
              flood(packet, packet_in, addy["10.2.5.50"]) #h50
            if dest_ip == "10.2.6.60":
              flood(packet, packet_in, addy["10.2.6.60"]) #h60
            if dest_ip == "10.2.7.70":
              flood(packet, packet_in, addy["10.2.7.70"]) #h70
            if dest_ip == "10.2.8.80":
              flood(packet, packet_in, addy["10.2.8.80"]) #h80
            if dest_ip == "108.24.31.112":
              flood(packet, packet_in, addy["108.24.31.112"]) #h_trust
            if dest_ip == "106.44.82.103":
              flood(packet, packet_in, addy["106.44.82.103"]) #h_untrust
            if dest_ip == "10.3.9.90":
              flood(packet, packet_in, addy["10.3.9.90"]) #h_server

          if port_on_switch == 7: # from h_server
            if dest_ip == "10.1.1.10":
              flood(packet, packet_in, addy["10.1.1.10"]) #h10
            if dest_ip == "10.1.2.20":
              flood(packet, packet_in, addy["10.1.2.20"]) #h20
            if dest_ip == "10.1.3.30":
              flood(packet, packet_in, addy["10.1.3.30"]) #h30
            if dest_ip == "10.1.4.40":
              flood(packet, packet_in, addy["10.1.4.40"]) #h40
            if dest_ip == "10.2.5.50":
              flood(packet, packet_in, addy["10.2.5.50"]) #h50
            if dest_ip == "10.2.6.60":
              flood(packet, packet_in, addy["10.2.6.60"]) #h60
            if dest_ip == "10.2.7.70":
              flood(packet, packet_in, addy["10.2.7.70"]) #h70
            if dest_ip == "10.2.8.80":
              flood(packet, packet_in, addy["10.2.8.80"]) #h80
            if dest_ip == "108.24.31.112":
              flood(packet, packet_in, addy["108.24.31.112"]) #h_trust
            if dest_ip == "106.44.82.103":
              flood(packet, packet_in, addy["106.44.82.103"]) #h_untrust
          
        # SWITCH 4
        elif switch_id == 4:
          # check dest_ip and forward it
          # from core
          if port_on_switch == 17:
            flood(packet, packet_in, 10) # to s3/core
          
          # from h_server
          if port_on_switch == 10:
            flood(packet, packet_in, 17) # to h_server
            

        # SWITCH 5
        elif switch_id == 5:
          # check dest_ip and forward it
          if dest_ip == "10.2.5.50":
            flood(packet, packet_in, 24) # to h50  
          elif dest_ip == "10.2.6.60":
            flood(packet, packet_in, 25) # to h60
          else:
            flood(packet, packet_in, 13) # to s3/core

        # SWITCH 6
        elif switch_id == 6:
          # check dest_ip and forward it
          if dest_ip == "10.2.7.70":
            flood(packet, packet_in, 26) # to h70
          elif dest_ip == "10.2.8.80":
            flood(packet, packet_in, 27) # to h80
          else:
            flood(packet, packet_in, 14) # to s3/core
        

      else: # ipv4 but not icmp
        print("ipv4 but not icmp")
        # dest_ip: receiver's ip address
        dest_ip = str(ipv4.dstip)
        # SWITCH 1
        if switch_id == 1:
          # check dest_ip and forward it
          if dest_ip == "10.1.1.10":
            flood(packet, packet_in, 20) # to h10
          elif dest_ip == "10.1.2.20":
            flood(packet, packet_in, 21) # to h20
          else:
            flood(packet, packet_in, 11) # to s3/core

        # SWITCH 2
        if switch_id == 2:
          # check dest_ip and forward it
          if dest_ip == "10.1.3.30":
            flood(packet, packet_in, 22) # to h30
          elif dest_ip == "10.1.4.40":
            flood(packet, packet_in, 23) # to h40
          else:
            flood(packet, packet_in, 12) # to s3/core

        # SWITCH 3/ CORE
        if switch_id == 3:

          # writing the firewall
          if port_on_switch == 5: # from h_untrust
            if dest_ip == "10.1.1.10":
              flood(packet, packet_in, addy["10.1.1.10"]) #h10
            if dest_ip == "10.1.2.20":
              flood(packet, packet_in, addy["10.1.2.20"]) #h20
            if dest_ip == "10.1.3.30":
              flood(packet, packet_in, addy["10.1.3.30"]) #h30
            if dest_ip == "10.1.4.40":
              flood(packet, packet_in, addy["10.1.4.40"]) #h40
            if dest_ip == "10.2.5.50":
              flood(packet, packet_in, addy["10.2.5.50"]) #h50
            if dest_ip == "10.2.6.60":
              flood(packet, packet_in, addy["10.2.6.60"]) #h60
            if dest_ip == "10.2.7.70":
              flood(packet, packet_in, addy["10.2.7.70"]) #h70
            if dest_ip == "10.2.8.80":
              flood(packet, packet_in, addy["10.2.8.80"]) #h80
            if dest_ip == "108.24.31.112":
              flood(packet, packet_in, addy["108.24.31.112"]) #h_trust
            if dest_ip == "10.3.9.90":
              drop(packet, packet_in) # drop h_server

          if port_on_switch == 6: # from h_trust
            if dest_ip == "10.1.1.10":
              flood(packet, packet_in, addy["10.1.1.10"]) #h10
            if dest_ip == "10.1.2.20":
              flood(packet, packet_in, addy["10.1.2.20"]) #h20
            if dest_ip == "10.1.3.30":
              flood(packet, packet_in, addy["10.1.3.30"]) #h30
            if dest_ip == "10.1.4.40":
              flood(packet, packet_in, addy["10.1.4.40"]) #h40
            if dest_ip == "10.2.5.50":
              flood(packet, packet_in, addy["10.2.5.50"]) #h50
            if dest_ip == "10.2.6.60":
              flood(packet, packet_in, addy["10.2.6.60"]) #h60
            if dest_ip == "10.2.7.70":
              flood(packet, packet_in, addy["10.2.7.70"]) #h70
            if dest_ip == "10.2.8.80":
              flood(packet, packet_in, addy["10.2.8.80"]) #h80
            if dest_ip == "106.44.82.103":
              flood(packet, packet_in, addy["106.44.82.103"]) #h_untrust
            if dest_ip == "10.3.9.90":
              drop(packet, packet_in) # drop h_server

          if port_on_switch == 1 or port_on_switch == 2: # from h10-h40
            if dest_ip == "10.1.1.10":
              flood(packet, packet_in, addy["10.1.1.10"]) #h10
            if dest_ip == "10.1.2.20":
              flood(packet, packet_in, addy["10.1.2.20"]) #h20
            if dest_ip == "10.1.3.30":
              flood(packet, packet_in, addy["10.1.3.30"]) #h30
            if dest_ip == "10.1.4.40":
              flood(packet, packet_in, addy["10.1.4.40"]) #h40
            if dest_ip == "10.2.5.50":
              flood(packet, packet_in, addy["10.2.5.50"]) #h50
            if dest_ip == "10.2.6.60":
              flood(packet, packet_in, addy["10.2.6.60"]) #h60
            if dest_ip == "10.2.7.70":
              flood(packet, packet_in, addy["10.2.7.70"]) #h70
            if dest_ip == "10.2.8.80":
              flood(packet, packet_in, addy["10.2.8.80"]) #h80
            if dest_ip == "108.24.31.112":
              flood(packet, packet_in, addy["108.24.31.112"]) #h_trust
            if dest_ip == "106.44.82.103":
              flood(packet, packet_in, addy["106.44.82.103"]) #h_untrust
            if dest_ip == "10.3.9.90":
              flood(packet, packet_in, addy["10.3.9.90"]) #h_server

          if port_on_switch == 3 or port_on_switch == 4: # from h50-h80
            if dest_ip == "10.1.1.10":
              flood(packet, packet_in, addy["10.1.1.10"]) #h10
            if dest_ip == "10.1.2.20":
              flood(packet, packet_in, addy["10.1.2.20"]) #h20
            if dest_ip == "10.1.3.30":
              flood(packet, packet_in, addy["10.1.3.30"]) #h30
            if dest_ip == "10.1.4.40":
              flood(packet, packet_in, addy["10.1.4.40"]) #h40
            if dest_ip == "10.2.5.50":
              flood(packet, packet_in, addy["10.2.5.50"]) #h50
            if dest_ip == "10.2.6.60":
              flood(packet, packet_in, addy["10.2.6.60"]) #h60
            if dest_ip == "10.2.7.70":
              flood(packet, packet_in, addy["10.2.7.70"]) #h70
            if dest_ip == "10.2.8.80":
              flood(packet, packet_in, addy["10.2.8.80"]) #h80
            if dest_ip == "108.24.31.112":
              flood(packet, packet_in, addy["108.24.31.112"]) #h_trust
            if dest_ip == "106.44.82.103":
              flood(packet, packet_in, addy["106.44.82.103"]) #h_untrust
            if dest_ip == "10.3.9.90":
              flood(packet, packet_in, addy["10.3.9.90"]) #h_server

          if port_on_switch == 7: # from h_server
            if dest_ip == "10.1.1.10":
              flood(packet, packet_in, addy["10.1.1.10"]) #h10
            if dest_ip == "10.1.2.20":
              flood(packet, packet_in, addy["10.1.2.20"]) #h20
            if dest_ip == "10.1.3.30":
              flood(packet, packet_in, addy["10.1.3.30"]) #h30
            if dest_ip == "10.1.4.40":
              flood(packet, packet_in, addy["10.1.4.40"]) #h40
            if dest_ip == "10.2.5.50":
              flood(packet, packet_in, addy["10.2.5.50"]) #h50
            if dest_ip == "10.2.6.60":
              flood(packet, packet_in, addy["10.2.6.60"]) #h60
            if dest_ip == "10.2.7.70":
              flood(packet, packet_in, addy["10.2.7.70"]) #h70
            if dest_ip == "10.2.8.80":
              flood(packet, packet_in, addy["10.2.8.80"]) #h80
            if dest_ip == "108.24.31.112":
              flood(packet, packet_in, addy["108.24.31.112"]) #h_trust
            if dest_ip == "106.44.82.103":
              flood(packet, packet_in, addy["106.44.82.103"]) #h_untrust
            if dest_ip == "10.3.9.90":
              flood(packet, packet_in, addy["10.3.9.90"]) #h_server
          
        # SWITCH 4
        if switch_id == 4:
          # check dest_ip and forward it
          # from core
          if port_on_switch == 10:
            flood(packet, packet_in, 17) # to s3/core
          
          # from h_server
          if port_on_switch == 17:
            flood(packet, packet_in, 10) # to h_server

        # SWITCH 5
        if switch_id == 5:
          # check dest_ip and forward it
          if dest_ip == "10.2.5.50":
            flood(packet, packet_in, 24) # to h50  
          elif dest_ip == "10.2.6.60":
            flood(packet, packet_in, 25) # to h60
          else:
            flood(packet, packet_in, 13) # to s3/core

        # SWITCH 6
        if switch_id == 6:
          # check dest_ip and forward it
          if dest_ip == "10.2.7.70":
            flood(packet, packet_in, 26) # to h70
          elif dest_ip == "10.2.8.80":
            flood(packet, packet_in, 27) # to h80
          else:
            flood(packet, packet_in, 14) # to s3/core

    else:
      print("not ipv4 \n")
      drop(packet, packet_in)

    return



  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)


    

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)