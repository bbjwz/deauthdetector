# deauthdetector
Some experimental python code that aims to protect your home network from deauth attacks which are commonly used for wlan wpa cracking. The idea is that if you just constantly listen on the channel of your own wlan and a deauth package is detected that this is a signal for something fishy going on. 
<br><br>
At some point I hit a roadblock because I also wanted to visualize all the relationships of network devices in my area so I could actually find out if one of my neighbors was sending me deauths.
<br><br>
I'm in no way good at python, networking, github or sqlite, I've uploaded this code after a request from some redditors.
<br><br>
Feel free to make additions or changes to this code. As this is also a learning project for me I'd like to do it the proper github way. 
<br><br>
# prerequisites
tshark <br>
python <br>
sqlite3 <br>
a sqlite database called caps.db <br>
a wireless network adapter that supports monitor mode <br>
<br><br>
# how it should work
It's been a while since I've played with this code so bear with me. 
<br>
create_tables.py creates the needed sqlite tables <br>
setmonitormode.py sets the wlan1 device to monitormode<br>
channelhopping.py automatically hops between the list of channels in de code<br>
parsefrompipe.py allows you to stream and parse the json output of tshark and write it to a database<br>
parsecaptures.py allows you to parse a capture file from wireshark that is exported to json.
<br><br>
# what needs to be done
The actual detecting and signaling of deauth packages <br>
The visualization of mac to mac communication
