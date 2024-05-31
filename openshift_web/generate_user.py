#!/usr/bin/python

##Gloabal varible configuration
#set gloable varible values
import sys
import subprocess
from optparse import OptionParser
import commands
import re

confirm_url="https://stg.openshift.redhat.com/app/email_confirm?key=w9btgjDswstFYKgIPjo6M0MXtMDXjWtPkJctiftX&emailAddress=test2Bc216%40redhat.com"

    
configfile="config.py"

def convert_file(source_file,target_file):
	f1 = open(target_file,'r')
	context1 = f1.read()
	f1.close
	f2 = open(source_file,'r')
	line = f2.readline().strip("\n")
	while line != """""":
	    #print line
	    re_obj1 = re.compile(r"(.*)=(.*)")
	    match_obj = re_obj1.match(line)
	    if match_obj != None:
	     key = match_obj.group(1)
	     val = match_obj.group(2)
	     print "key: %s; val: %s" %(key, val)
	     re_obj2 = re.compile(r"^%s=.*$" %(key), re.M)
		#print re_obj2.findall(context)
	     context1 = re_obj2.sub("%s=%s" %(key,val), context1)
	    else:
             print "no match is found for the line: %s" %(line)
	     break

	    line = f2.readline().strip("\n")
	f3 = open(target_file,'w')
	f3.write(context1)
	f3.close

def conf_file_parser(conf_file):
    new_context=""
    myfile = open(conf_file,'r')
    line=myfile.readline()
    while line != """""":
        line=line.replace('"','\\"')
        line=line.replace("'","\\'")
        new_context=new_context+line
        line=myfile.readline()
    myfile.close

    tmp_file = open(conf_file,'w')
    tmp_file.write(new_context)
    tmp_file.close
    return conf_file

def register_new_user():
    '''
    cmd="./register_random -p  -d 2>debug1.log"
    (ret,output)=commands.getstatusoutput(cmd)
    print output
    new_userlist = [output]
    for i in range(3):
        (ret,output)=commands.getstatusoutput(cmd)
        print output
        new_userlist = new_userlist + [output]
    '''
    cmd="./register_random  -c -p  -d 2>debug.log"
    (ret,output)=commands.getstatusoutput(cmd)
    print output
    #new_userlist = new_userlist + [output.split("\n")[0]]
    __confirm_url = output.split("\n")[1]
    return __confirm_url

if __name__ == "__main__":
    _confirmemail=register_new_user()
    print _confirmemail
  
