				Extracting Client-provider Relationship between Autonomous Systems from RIP Atlas Using Gao-Rexford Model
										        Authors: Rathish Das and Sarthak Ghosh
========================================================================================================================================================
Implementation Details:
-------------------------------
Language used : Python 2.7
Libraries used: 1) pygeoip
				2) cymruwhois
				

SetUp:
-------------------------------
We need to install python-cymruwhois first.

1) Extract the file python-cymruwhois-master.zip and go to the directory $\python-cymruwhois-master\python-cymruwhois-master\
2) python setup.py build
3) python setup.py install

				
How to Run:
-------------------------------
$> python ASRelation.py <input_file.json>  <output_file.txt>
	eg, $>python ASRelation.py RIPE-Atlas-1st-measurement-3681625.json  ASRelationship.txt
				

Input Collection:
-------------------------------
To run this program first one needs to collect a traceroot file in .json format. Please follow the below steps-

1) Browse the URL https://atlas.ripe.net/measurements/
2) Go to Public or Built-in section.
3) Click on some probe ID.
4) Upon opening probe page, click the result tab.
5) Specify Start and Stop Date if applicable.
6) Click Download 

Algorithm:
-------------------------------
1) In the traceroute dump file, the IP addresses of the hops are listed. 
2) We have used the json library and parsed the traceroute dump files (obtained from RIPE Atlas) 
	and collected a path consisting of IP addresses that are traversed to reach a probe destination.
3) Once we get a collection of such paths composed of IP addresses, we use the GeoIPASNum.dat database
    and pygeoip library to query the AS ID number and AS name field from the IP address.
4) So, now, we have the path of ASes that are traversed to probe a destination. This enables us to create 
	a substantial collection of AS paths to hypothesize inter-AS relationships.
5) This problem now resembels to maximum independent set which is NP-Complete.
6) There is a polynomial time reduction from maximum independent set to "Type of Relationship" problem. 
6) We solve this by reducing to implementing a heuristics for the "Type of Relationship" problem (SCC.py).  