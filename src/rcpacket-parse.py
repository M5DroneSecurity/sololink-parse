#import json for load() and matplot for graph
#both internal libraries

#this is from david's data parser

import json
import pandas as pd
import numpy as np
'''
from xml.dom import minidom
'''

''' Only Change This!! '''
json_directory = '../data/'
json_filename = 'solo-20200223-trial3-rcpackets'
''' Only Change This!! '''


''' Location of Data for Parsing '''
json_location = json_directory + json_filename + '.json'

''' Initialize Relevant Fields '''
ip_src = []
ip_dst = []
data_len = []
data_data = []
count = 0
dead = 0

''' Load JSON file '''
print("Grabbing JSON: ", json_location)
with open(json_location) as src_file:
    src_loader = json.load(src_file)
    # print(src_loader)

    ''' Parse through JSON file for specific information'''
    for packet in src_loader:
        try:
            packet_array = packet['_source']['layers']['data']['data.data'].split(':')
            if packet['_source']['layers']['udp']['udp.srcport'] == '5005':
                ip_src.append(packet['_source']['layers']['ip']['ip.src'])
                ip_dst.append(packet['_source']['layers']['ip']['ip.dst'])
                data_len.append(packet['_source']['layers']['data']['data.len'])
                data_data.append(packet['_source']['layers']['data']['data.data'])
                count += 1
        except KeyError:
            print("Failed to append Data, KeyError. Packet " + str(count))
            count += 1
            dead += 1
    print("Lost Packets ", dead)
    # for n in range(len(src_loader)):
    #     print("DEBUG src_loader:  {}\t{}".format(data_len[n], data_data[n]))

''' Create a 2D Array that contains shows packets by split byte-fields '''
split_data = []
for dat in range(len(data_data)):
    split_data.append(data_data[dat].split(':'))
    # print(split_data[dat])

# print("DEBUG: Length of split_data is {}".format(split_data))
print("DEBUG: Length of data_data is {}".format(len(data_data)))


'''
First, lets split these data into rc packet fields
Serialization format: https://www.google.com/url?q=https%3A%2F%2Fgithub.com%2FArduPilot%2Fardupilot%2Fpull%2F6708%2Fcommits%2Fed08d4f66b8b44b233a33a95e489abe0229172cd&sa=D&sntz=1&usg=AFQjCNHv1ViqeX0-J6VzC2axUNz1MglNpA
'''

''' Declare arrays for each field '''
timestamp = []
rc_seq = []
ch1 = []
ch2 = []
ch3 = []
ch4 = []
ch5 = []
ch6 = []
ch7 = []
ch8 = []
duplicates = 0
unique_rcPackets = 0

''' Store data in these field arrays '''
for n in range(len(data_data)):
    ''' filter duplicates '''
    if split_data[n][0:13] != split_data[n-1][0:13]:
        timestamp.append(' '.join(split_data[n][0:4]))
        rc_seq.append(split_data[n][4])
        ch1.append(split_data[n][5])
        ch2.append(split_data[n][6])
        ch3.append(split_data[n][7])
        ch4.append(split_data[n][8])
        ch5.append(split_data[n][9])
        ch6.append(split_data[n][10])
        ch7.append(split_data[n][11])
        ch8.append(split_data[n][12])
        unique_rcPackets += 1
    else:
        duplicates += 1

print("Packets processed: {}".format(unique_rcPackets))
print("Duplicate packet count: {}".format(duplicates))

clean = pd.DataFrame(np.column_stack([timestamp, rc_seq, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8]),
                     columns=['timestamp [0:4]', 'rc_seq', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8'])

'''
Let's display parsed data and occurance count in an excel file (.xlsx)
NOTE: I can't autofit columns through the script but here's how to do it manually:
https://support.office.com/en-us/article/change-the-column-width-and-row-height-72f5e3cc-994d-43e8-ae58-9774a0905f46
'''
clean.to_excel('../results/'+'rcPackets-'+json_filename+'.xlsx')
