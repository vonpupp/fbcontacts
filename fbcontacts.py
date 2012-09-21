#!/usr/bin/python

#   Project:			fbcontacts
#   Language:			Python
#
#   License: 			GNU Public License
#       This file is part of the project.
#	This is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#       without even the implied warranty of MERCHANTABILITY or
#       FITNESS FOR A PARTICULAR PURPOSE.
#       See the GNU General Public License for more details.
#       <http://www.gnu.org/licenses/>
#
#   Author:			Albert De La Fuente (www.albertdelafuente.com)
#   E-Mail:			http://www.google.com/recaptcha/mailhide/d?k=01eb_9W_IYJ4Pm_Y9ALRIPug==&c=L15IEH_kstH8WRWfqnRyeW4IDQuZPzNDRB0KCzMTbHQ=
#
#   Description:		Creates a CSV file with facebook contacts data (name and email)
#                               from yahoo TrueSwitch
#
#   Limitations:		I've done this in about an hour, so don't expect too much!
#       - Unicode characters are not correctly handled, patches are welcome!
#   Database tables used:	None 
#   Thread Safe:	        No
#   Extendable:			No
#   Platform Dependencies:	Linux (openSUSE used)
#   Compiler Options:		
"""
    Creates a CSV file with facebook contacts data (name and email) from yahoo TrueSwitch

    PROCEDURE:
        * Requirement: You need a yahoo & hotmail mail account, create them if needed.
        
        AT HOTMAIL:
        * At hotmail go to people (up left corner)
        * Click on the Facebook icon
        * Click on okay, to authorize facebook to share contacts data with hotmail
        
        AT YAHOO:
        * At yahoo mail go to contacts
        * Click on Import contacts
        * Click on the hotmail icon
        * Put your credentials and check "I give Yahoo! permission..."
        * The "Step 2" window will show you a list of your contacts. Save the page with save page as
        * It will create a /transfercontacts_files folder with an index.html file within
            This is going to be the program input!

    Command Line Usage:
        python fbcontacts.py ./transfercontacts_files/index.html
        
    Author:			Albert De La Fuente (www.albertdelafuente.com)
    E-Mail:			http://www.google.com/recaptcha/mailhide/d?k=01eb_9W_IYJ4Pm_Y9ALRIPug==&c=L15IEH_kstH8WRWfqnRyeW4IDQuZPzNDRB0KCzMTbHQ=
    
    Why I've done this:         I've done this because I believe that I own my fb account data,
                                and I should be able to export it if I want.
"""

import argparse, codecs, sys, mmap, re, csv
#import os
from vlog import vlogger

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

def split_on_caps(str):
    rs = re.findall('[A-Z][^A-Z]*',str)
    fs = ""
    for word in rs:
        fs += " "+word
    return fs

class fbcontactdata():
    def __init__(self, fullname, first, middle, last, email):
        # Public
        self.fullname = fullname
        self.first = first
        self.middle = middle
        self.last = last
        self.email = email

class fbcontactsparser():
    def __init__(self, filename):
        # Public
        self.filename = filename
        self.outfile = 'out.csv'
        self.clist = []
        
        # Init vlogger
        self.__verbosity = VERB_MAX
        self.vlog = vlogger(self.__verbosity, sys.stdout)
        #self.vlog = self.__log()
        
        # Init mmap
        self.__file = codecs.open(filename, encoding='utf-8', mode='r') # open(filename, 'r')
        self.vlog(VERB_MIN, "opening file: %s" % filename)
        self.__f = mmap.mmap(self.__file.fileno(), 0, access=mmap.ACCESS_READ)
        self.__f.seek(0) # rewind
        pass
    
    def parse(self):
        """
        Fills the funlist list with all the parsed functionalities based on the index.
        """
        self.vlog(VERB_MED, "-> %s" % __name__)
        
        # Find the position of the begining tag
        #begintag = "Lista Completa de Funcionalidades"
        #beginloc = self.__f.find(begintag)
        ## Find the position of the end tag
        #endtag = "LISTA COMPLETA DE FUNCIONALIDADES"
        #endloc = self.__f.find(endtag, beginloc+1)
        ## Set the cursor at the begining tag & skip the first line
        #self.__f.seek(beginloc)
        self.__f.seek(0)
        self.__f.readline()
        loc = self.__f.tell()
        endloc = self.__f.size() - 1
        
        #self.vlog(VERB_MAX, "beginloc = %d" % beginloc)
        #self.vlog(VERB_MAX, "endloc = %d" % endloc)
        
        self.clist = []
        count = 0
        biggestline = ''
        while (loc < endloc):
            line = self.__f.readline()
            self.vlog(VERB_MAX, "reading line '%s' bytes = %d" % (line, loc))
            if len(line) > len(biggestline):
                biggestline = line
            loc = self.__f.tell()
            
        #self.vlog(VERB_MED, "<- getfunlist()")
        #self.vlog(VERB_MED, "<- %s" % __name__)
        
        #self.vlog(VERB_MAX, "biggestline = %s" % (biggestline))
        
        if self.outfile is not '':
            fh = open(self.outfile, 'wb')
            #fh = codecs.open(self.outfile, "wb", "utf-8")

            #fh = codecs.open(self.outfile, 'wb', encoding="utf-8")
        else:
            fh = sys.stdout

#        csvhdlr = csv.writer(fh, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #csvhdlr.writerow("Name,Given Name,Additional Name,Family Name,Yomi Name,Given Name Yomi,Additional Name Yomi,Family Name Yomi,Name Prefix,Name Suffix,Initials,Nickname,Short Name,Maiden Name,Birthday,Gender,Location,Billing Information,Directory Server,Mileage,Occupation,Hobby,Sensitivity,Priority,Subject,Notes,Group Membership,E-mail 1 - Type,E-mail 1 - Value".split(','))        
        
        clist = biggestline.split('&quot;}]},')
        for contact in clist:
            fullname = ''
            first = ''
            middle = ''
            last = ''
            email = ''
            
            m = re.compile(r'&quot;name&quot;:&quot;(.*?)&quot;,').search(contact)
            if m:
                fullname = m.group(1)
            
            m = re.compile(r'{&quot;email&quot;:&quot;(.*?)&quot;,').search(contact)
            if m:
                email = m.group(1)
            
            m = re.compile(r'&quot;first&quot;:&quot;(.*?)&quot;,').search(contact)
            if m:
                first = m.group(1)
                
            m = re.compile(r'&quot;last&quot;:&quot;(.*?)&quot;}').search(contact)
            if m:
                last = m.group(1)
            
            if last is not '':
                m = re.compile(r'&quot;middle&quot;:&quot;(.*?)&quot;,').search(contact)
            else:
                m = re.compile(r'&quot;middle&quot;:&quot;(.*?)&quot;},').search(contact)
            if m:
                middle = m.group(1)
            
            fullname = re.sub( '\s+', ' ', split_on_caps(fullname)).strip()
            
            contact = fbcontactdata(fullname, first, middle, last, email)
            self.clist.append(contact)
            
            self.vlog(VERB_MAX, "---")
            self.vlog(VERB_MAX, "fullname = %s" % (fullname))
            self.vlog(VERB_MAX, "first = %s" % (first))
            self.vlog(VERB_MAX, "middle = %s" % (middle))
            self.vlog(VERB_MAX, "last = %s" % (last))
            self.vlog(VERB_MAX, "email = %s" % (email))
            
            #row = fullname + ',,,,,,,,,,,,,,,,,,,,,,,,,,fbcontacts ::: * My Contacts,* Home,' + email
            #csvhdlr.writerow(row.split(','))
            #,Yasmin,L\u00f3pez,L\u00f3pez,,,,,,,,,,,,,,,,,,,,,,,fbcontacts ::: * My Contacts,* Home,yasminlq@msn.com
            
            #print('first = 'first + "|" + middle + "|" + last + "|" + email)
            #print(contact)
        #print clist
        
        #self.vlog(VERB_MAX, "result = %s" % (self.clist))
        #self.funlist += [result]
        #return self.funlist
    
    def writecsv(self):
        if self.outfile is not '':
            fh = open(self.outfile, 'wb')
            #fh = codecs.open(self.outfile, "wb", "utf-8")

            #fh = codecs.open(self.outfile, 'wb', encoding="utf-8")
        else:
            fh = sys.stdout

        csvhdlr = csv.writer(fh, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow("Name,Given Name,Additional Name,Family Name,Yomi Name,Given Name Yomi,Additional Name Yomi,Family Name Yomi,Name Prefix,Name Suffix,Initials,Nickname,Short Name,Maiden Name,Birthday,Gender,Location,Billing Information,Directory Server,Mileage,Occupation,Hobby,Sensitivity,Priority,Subject,Notes,Group Membership,E-mail 1 - Type,E-mail 1 - Value".split(','))        
        for contact in self.clist:
            #csvhdlr.writerow(dict((vname, vtype, vnotes, vstereotype, vauthor, valias, vgenfile.encode('utf-8')) for vname, vtype, vnotes, vstereotype, vauthor, valias, vgenfile in row.iteritems()))
            row = contact.fullname + ',,,,,,,,,,,,,,,,,,,,,,,,,,fbcontacts ::: * My Contacts,* Home,' + contact.email
            csvhdlr.writerow(row.split(','))
            #self.logv(2, "writecsv().row = " + str(row))
        #self.logv(2, "writecsv().outfile = " + self.outfile)


def main(args):
    parser = fbcontactsparser(args.filename)
    parser.parse()
    parser.writecsv()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__) #"Creates a CSV file with facebook contacts data (name and email) from yahoo TrueSwitch")
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args)
