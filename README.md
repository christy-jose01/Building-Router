# Building-Router
This repository builds a router. It contains two programming files, the details are below. This router is built using Python and utilizes the pox library.

## Files: 
- final_skel.py: This file contains all of the code for the topology of the network and connections.
- finalcontroller_skel.py: This file contains all of the code on processing the packet, forwarding the packet through the network, and the code for the firewall.
- project.pdf: This file contains all of the screenshots and all of the explanations of how the requirements of the project were fulfilled and how they were tested.

## Running the project:
1. Save the final_skel.py file in your home directory
2. Save the finalcontroller_skel.py file in ~/pox/pox/misc directory
3. In one terminal run the command sudo ~/pox/pox.py misc.finalcontroller_skel
4. In another terminal run the command sudo python ~/final_skel.py, which opens mininet
5. In terminal 2, run any mininet commands such as pingall, dpctl dump-flows, iperf
