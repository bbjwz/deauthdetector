# deauthdetector
Some experimental python code that aims to protect your home network from deauth attacks which are commonly used for wlan wpa cracking. The idea is that if you just constantly listen on the channel of your own wlan and a deauth package is detected that this is a signal for something fishy going on. 

At some point I hit a roadblock because I also wanted to visualize all the relationships of network devices in my area so I could actually find out if one of my neighbors was sending me deauths.

I'm in no way good at python, networking, github or sqlite, I've uploaded this code after a request from some redditors.

Feel free to make additions or changes to this code. As this is also a learning project for me I'd like to do it the proper github way. 

# prerequisites
tshark
python
sqlite3
a sqlite database called caps.db
a wireless network adapter that supports monitor mode

# how it should work
It's been a while since I've played with this code so bear with me. 

create_tables.py creates the needed sqlite tables 
setmonitormode.py sets the wlan1 device to monitormode
channelhopping.py automatically hops between the list of channels in de code
parsefrompipe.py allows you to stream and parse the json output of tshark and write it to a database


parsecaptures.py allows you to parse a capture file from wireshark that is exported to json.

# what needs to be done
The actual detecting and signaling of deauth packages
The visualization of mac to mac communication
