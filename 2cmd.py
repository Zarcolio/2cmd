#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import signal
import os
from termcolor import colored
import time
import multiprocessing 

def signal_handler(sig, frame):
        sys.stderr.write("\nCtrl-C detected, terminating all workers...\n")
        pool.terminate()
        sys.exit(0)

def FileNameSan(sFileName):
    sFileName = sFileName.replace("://", "-")
    sFileName = sFileName.replace(":", "-")
    sFileName = sFileName.replace("/", "-")
    sFileName = sFileName.replace("&", "-")
    sFileName = sFileName.replace("?", "-")
    sFileName = sFileName.replace("*", "-")
    return sFileName

def escapeString(sString):
    sString = sString.replace("$","\$", len(sString))
    sString = sString.replace("&","\&", len(sString))
    sString = sString.replace(";","\;", len(sString))
    sString = sString.replace("\"","\\\"", len(sString))
    #sString = sString.replace("","", len(sString))
    return sString

def execCmd(sCmd):
    if args.verbose:
        sys.stderr.write((colored(sCmd,"green"))+"\n")
    os.system(sCmd)


def getFullDir(sFile):
    # if no path is provided, assume scriptdir/2cmd.xmpls:
    if "/" in sFile:
        sPathToFile = os.path.abspath(sFile)
    else:
        sPathToFile = os.path.dirname(os.path.realpath(sys.argv[0])) + "/2cmd.xmpls/" + sFile
    return sPathToFile 

signal.signal(signal.SIGINT, signal_handler)

# Get some commandline arguments:
parser = argparse.ArgumentParser(description="This script takes input lines from stdin and inserts them in the commands provided in the commands file. This way you can execute a certain command many times. For example you can take screen shots of URLs with cutycapt provided by output of another command.")
parser.add_argument("cmd", help="File containing one or more commands that should be executed. If no path is provided, a file in scriptdir/2cmd.xmpls is assumed. Use $2cmd$ or $2cmdsan$ in lowercase in each command line. $2cmd$ is replaced with each line from input. Use $cmdsan$ to sanitize a string for use in a filename.")
parser.add_argument("-2", "--second", help="Pass a second variable to the script to run.")
parser.add_argument("-t", "--timeout", help="Wait x milliseconds between commands.")
parser.add_argument("-v", "--verbose", help="In green, show the commands that are created from stdin and the provide config file.", action="store_true")
parser.add_argument("-w", "--workers", help="Defines how many worker threads execute the commands parallelly.", default=1)
args = parser.parse_args()

if not args.cmd:
    parser.print_help(sys.stderr)
    sys.exit(1)

try:
    f = open(getFullDir(args.cmd), 'r')
    aCmds = f.readlines()
    f.close()
except FileNotFoundError:
    print ("File " + getFullDir(args.cmd) + " not found, exiting...")
    sys.exit(1)

iFirst = 0
pool = multiprocessing.Pool(int(args.workers))
 
for strInput in sys.stdin:
    if args.timeout:
        if iFirst == 1:
            time.sleep (int(args.timeout)/1000)
        iFirst = 1  
        
    for sCmd in aCmds:
        sCmd = sCmd.strip()
        if not strInput.strip():
            continue
        
        strInputSan = FileNameSan(strInput)
        sCmd = sCmd.replace("$2cmdsan$", strInputSan, len(sCmd))

        sCmd = sCmd.replace("$2cmd$", strInput, len(sCmd))
        if args.second:
            sCmd = sCmd.replace("$2nd$", args.second, len(sCmd))

        sCmd = sCmd.replace("\n", "", len(sCmd))
        sCmd = escapeString(sCmd)
        
        pool.apply_async(execCmd, args = (sCmd, ))

pool.close()
pool.join()
