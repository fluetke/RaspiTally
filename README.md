# RaspiTally
Simple democratic tally using the raspberry pi

Ok, so basically this is the software package developed during my Master thesis in Digital Media.
I did an exploratory study to identify the potential of director-less multicam setups using a 
voting system between camera operators to identify the next shot to be switched to the live feed.

The system consists of 1 raspberry-pi acting as a server and an apple-script client to control Wirecast, 
a streaming software for OSX. Each camera gets an additional viewfinder screen, which also contains a raspberry 
pi and acts as tally-client and remote control surface for the Wirecast-switcher running on the streaming pc.

When a camera goes live, the raspberry pi connected to it's screen will switch on the red tally-light on top of 
a camera to indicate it's status to the presenters in front of the camera.

The hardware part that was developed in parallel to the software system, basically consists of rail-mountable 
monitor and tally-light cases, as well as battery mounts for Sony NF-batteries so the whole thing can also be used
wirelessly in the field. 

Unfortunately I haven't yet found the time to overhaul the whole system and adapt it to OBS, the opensource 
broadcasting solution, so at this point take it as a proof of concept.
