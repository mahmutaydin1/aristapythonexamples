#In this script, we have 100 leaf switches.

import pyeapi
import pprint

switches =[]
Problemliolanlar=[]
Po100_Problemliolanlar=[]
Mlag_LLDP_Problemiolanlar=[]
BGP_Problemiolanlar=[]
vericekme_problemiolanlar=[]
problemli_cihazlar=[]
i=101


while i<201:
    fourh_octet=i
    IP= "10.129.34."+str(fourh_octet)
    i = i+1
    switches.append(IP)


for i in switches:
    try:
        node = pyeapi.connect(transport="https", host=i,username="xxxx", password="xxx!", port=None)
        hostname = node.execute(["show hostname"])
        cihazin_adi = hostname['result'][0]['hostname']
        leafnumber= cihazin_adi.split("-")

        lldp = node.execute(["show lldp neighbors"])
        cihazdaki_komsuluk = list(lldp['result'][0]['lldpNeighbors'])
        cihazdaki_komsuluk.reverse()
        cihazdaki_lldp_sayisi = len(cihazdaki_komsuluk)

        cvx=node.execute(["show management cvx"])



        po100 = node.execute(["show interfaces  port-Channel 100 status"])

        bgp = node.execute(["show ip bgp summary"])
        bgppeer = bgp['result'][0]['vrfs']['default']['peers']

        print
        print"***************************************"
        print "cihazin adi:", cihazin_adi
        print "cihazdaki LLDP sayisi:",cihazdaki_lldp_sayisi
        print "cihazin peer komsusu:",cihazdaki_komsuluk[2]['neighborDevice']
        print "Port-channel100:", po100['result'][0]['interfaceStatuses']['Port-Channel100']['linkStatus']
        list_neighbor_hostname=cihazdaki_komsuluk[2]['neighborDevice'].split("-")
        list_neighbor_hostname_2= cihazdaki_komsuluk[3]['neighborDevice'].split("-")


    except:
        print "Veri Cekilemedi"
        vericekme_problemiolanlar.append(i)
    if po100['result'][0]['interfaceStatuses']['Port-Channel100']['linkStatus'] == "connected":

        list_neighbor_hostname=cihazdaki_komsuluk[2]['neighborDevice'].split("-")
        list_neighbor_hostname_2= cihazdaki_komsuluk[1]['neighborDevice'].split("-")



        try:
            if int(leafnumber[7])-int(list_neighbor_hostname[7])==1 or int(leafnumber[7])-int(list_neighbor_hostname[7])==-1:
                print " 1. Mlag peer komsuluk dogru"
            else:
                print " 1.Mlag Peerde problem var"
                Mlag_LLDP_Problemiolanlar.append(cihazin_adi)
        except:
            print "1.LLDPde hata var"
            Mlag_LLDP_Problemiolanlar.append(cihazin_adi)

        try:
            if int(leafnumber[7])-int(list_neighbor_hostname_2[7])==1 or int(leafnumber[7])-int(list_neighbor_hostname_2[7])==-1:
                print " 2. Mlag peer komsuluk dogru"
            else:
                print "2.Mlag Peerde Problem var"
                Mlag_LLDP_Problemiolanlar.append(cihazin_adi)
        except:
            print "2.LLDPde hata var"
            Mlag_LLDP_Problemiolanlar.append(cihazin_adi)


    elif po100['result'][0]['interfaceStatuses']['Port-Channel100']['linkStatus'] != "connected":
        print " Po100 da problem var"
        Po100_Problemliolanlar.append(cihazin_adi)
    print "LLDP KOMSULUKLARI"
    for t in cihazdaki_komsuluk:
        print t['neighborDevice'], ":", t['port']
    print "BGP KOMSULUKLARI"
    try:
        for peer in bgppeer:
            print peer,":",bgp['result'][0]['vrfs']['default']['peers'][peer]['peerState']
            try:
                if bgp['result'][0]['vrfs']['default']['peers'][peer]['peerState'] != "Established":
                    BGP_Problemiolanlar.append(cihazin_adi)
            except:
                BGP_Problemiolanlar.append(cihazin_adi)
                print "Bgp peerlerde hata var"
    except:
        print "BGPde hata var"
        BGP_Problemiolanlar.append(cihazin_adi)

    print"***************************************"
    print


print  "Herhangi bir veri cekme problemi olan cihazlar:",vericekme_problemiolanlar
print  "PO100 Problemi olanlar:",Po100_Problemliolanlar
print "Mlag LLDP Problemi olanlar:",Mlag_LLDP_Problemiolanlar
print "BGP Problemi olanlar:",BGP_Problemiolanlar



