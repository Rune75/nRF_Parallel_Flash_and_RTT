#!/usr/bin/env python3
import multiprocessing 
import pylink
import FlashAndprovision as fp #Import Flash and config module

#hexFile='./nRF_hexFiles/rttShell840.hex'
hexFile='./nRF_hexFiles/rttShell833.hex'

def flashProcess(serialnumbers):
    fp.FLasAndConfig(serialnumbers,hexFile)

#------------------------------------------
#-- Main 
#------------------------------------------

#-- Get a list of connected JLinks serial numbers to run in parallel.
jlinkSerialNumbers = fp.getJLinkSerials(pylink.JLink())    

#- Execute Jlink programming and RTT configuration in parallel 
with multiprocessing.Pool() as pool: 
    pool.map(flashProcess, jlinkSerialNumbers)

print("Finished paralell programming.")


