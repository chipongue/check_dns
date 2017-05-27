#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script to check DNS changes

Creation date: 10/02/2017
Date last updated: 19/03/2017

Nagios check_dns plugin

* 
* License: GPL
* Copyright (c) 2017 DI-FCUL
* 
* Description:
* 
* This file contains the check_dnsbl plugin
* 
* Use the nrpe program to check the application are installed in remote host.
* 
* 
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* 
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import sys
import urllib.request
from optparse import OptionParser
import ipaddress
import socket

__author__ = "\nAuthor: Raimundo Henrique da Silva Chipongue\nE-mail: fc48807@alunos.fc.ul.pt, chipongue1@gmail.com\nInstitution: Faculty of Science of the University of Lisbon\n"
__version__= "1.0.0"

# define exit codes
ExitOK = 0
ExitWarning = 1
ExitCritical = 2
ExitUnknown = 3

def check_connectivity():
    try:
        urllib.request.urlopen('http://194.210.238.163', timeout=2)
        return True
    except urllib.request.URLError:
        return False

def dns_f(opts):
    if check_connectivity():
        
        address_found =[]
        iplist = []
        domain = opts.hostname
        domain = domain.replace("https://", "")
        domain = domain.replace("http://", "")
        domain = domain.replace("www.", "")
        try:       
            answers = os.popen("dig +short %s @%s"%(domain, opts.dnsserver)).read()
        except:
            print("Connot query dns")
            sys.exit(ExitUnknown)
                           
        if answers != "" or answers != 0:    
            address_found.extend([i for i in answers.split("\n")])
            error = 0
            n = -1
            for ip in address_found:
                n = n +1
                try:
                    ipaddress.ip_address(address_found[n])
                    iplist.extend([i for i in str(address_found[n]).split(",")])      
                except:
                    error = error + 1
                    
        hostaddress = []
        hostaddress.extend([opts.hostaddress])
        try:
            match = list(set(hostaddress).intersection(iplist))
            match_item = str(match[0])
        except:
            match_item = 0 
        if opts.hostaddress == match_item:
            print("The IP Address %s corresponds to the domain name %s" %(match_item, domain))
            sys.exit(ExitOK)
        else:
            print("The IP Address %s does not match the domain name %s"%(opts.hostaddress, domain))
            sys.exit(ExitCritical)  
    else:
        print("Error, check you internet connection")
        sys.exit(ExitUnknown)

def main():
    parser = OptionParser("usage: %prog [options] ARG1 ARG2 FOR EXAMPLE: -I 192.168.0.1 -H domain.com")
    parser.add_option("-H","--hostname", dest="hostname", help="Specify the Domain Name you want to check")
    parser.add_option("-I","--hostaddres", dest="hostaddress", help="Specify the IP you want to check")
    parser.add_option("-d","--dnsserver", type=str, default="8.8.8.8", dest="dnsserver",
                      help="Specify the DNS server you need to use for check DNSSEC, for example: -d 127.0.0.1, default value is 8.8.8.8")
    parser.add_option("-V","--version", action="store_true", dest="version", help="This option show the current version number of the program and exit")
    parser.add_option("-A","--author", action="store_true", dest="author", help="This option show author information and exit")
    (opts, args) = parser.parse_args()
    
    if opts.author:
        print(__author__)
        sys.exit()
    if opts.version:
        print("check_dns.py %s"%__version__)
        sys.exit()
    if opts.hostname and opts.hostaddress:
        try:
            ip = ipaddress.ip_address(opts.hostaddress)
        except:
            parser.error("This application requires a valid IP Address.")
    else:
        parser.error("Usage: %s -H <hostname> -I <IP Address>"%sys.argv[0])
    dns_f(opts)
 
if __name__ == '__main__':
    main()
