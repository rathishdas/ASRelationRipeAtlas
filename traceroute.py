__author__ = 'RATHISH DAS and Sarthak Ghosh'
#!/usr/bin/env python


def getTraceRoute(jsonFile):
  import json
  import sys
  import pygeoip
  from AtlasUtils import *
  from cymruwhois import Client
  c=Client()
  inFile = jsonFile
  outFile = "tmpASPath.txt"
  my_file = open(outFile, "w")
  asnDict = open("asnDict.txt","w")



  with open(inFile) as data_file:
      data = json.load(data_file)
  ### use GeoIPASNum.dat if system is not connected to Internet. This is a offline database of ip-to-AS mapping
  gi = pygeoip.GeoIP('GeoIPASNum.dat')
  #
  if is_valid_ipv4(data[0]["from"]):
    gi = pygeoip.GeoIP('GeoIPASNum.dat')
  else :
      gi = pygeoip.GeoIP('GeoIPASNumv6.dat')

  for index in range(len(data)):

    tmpASPath = ""

    for cnt in range(len(data[index]["result"])):

      if data[index]["result"][cnt].has_key("error"):
        print data[index]["result"][cnt]["error"]
      else:
        for resultrttindex in range(len(data[index]["result"][cnt]["result"])):
          #print data[index]["result"][cnt]["result"][resultrttindex]
          from_val = "*"
          asn_val = False

          if data[index]["result"][cnt]["result"][resultrttindex].has_key("from"):
            from_val = data[index]["result"][cnt]["result"][resultrttindex]["from"]
            tmp = "None"
            r=c.lookup(from_val)
            asn_val = r.asn+"$"+r.owner

        print "%s :--> %s" % (from_val, asn_val)
        if isinstance(asn_val, str) and not 'NA' in asn_val:
          asnDict.write(asn_val+"\n")

        if isinstance(asn_val, str) and not 'NA' in asn_val:
          s = tmpASPath.split(" ")

          if not s[len(s)-2] == r.asn:
            tmpASPath = tmpASPath + r.asn + " "
    my_file.write(tmpASPath + "\n")

  my_file.close()
  asnDict.close()

