# sololink-parse
This repo contains scripts written to aid in the parsing and analysis of 3DR Solo (sololink) network traffic.

## rcpacket-parse.py
This script is written to parse RC packets collected from the 3DR Solo. It is a modified version of the DataParser written for MAVLink packets by D Liang.  
Input: specified .json file of udp port 5005 data located in /data folder.  
Output: .xlsx file of sorted RC packet data as defined by STM32 RC packet structures in OpenSolo Github repo.
