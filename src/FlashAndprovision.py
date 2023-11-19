#!/usr/bin/env python3

import pylink
import sys
import time
import logging
import re

target_device='nRF52840_xxAA'

def setupLogger(serial_number):
    extra = {'serial':str(serial_number)}
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="%(asctime)s.%(msecs)03d %(levelname)s %(serial)s: %(message)s", datefmt='%Y-%m-%d-%H:%M:%S')
    
    #- sett loging level for std Out
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    #- sett loging level for file
    fh = logging.FileHandler(str(serial_number)+"_log.log", "w")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(ch)
    log.addHandler(fh)
    log = logging.LoggerAdapter(log, extra)
    return log


def rtt_command(jlink, command,log):
    log.info("RTT Command: \"%s\"", command)
    try:
        jlink.connected()
        jlink.rtt_read(0,1024) #Empty RTT buffer
        bytes = list(b"\x0A\x00" + bytearray(command, "utf-8") + b"\x0A\x00")
        jlink.rtt_write(0, bytes)
    except Exception:
        log.error("IO write exception, exiting...")
        raise
    
    ##----------------- Compose desired response from RTT shell
    desiredResponse = re.split("\s", command)
    if desiredResponse[1] == "set":
        desiredResponse = " ".join([desiredResponse[2], "ok:", desiredResponse[3]])
    elif desiredResponse[1] == "get":
        desiredResponse = " ".join([desiredResponse[2], "ok"])
    else:
        desiredResponse = " ".join([desiredResponse[1], "ok"])

    log.debug("Desired response: \"%s\"", desiredResponse)
        
    ##----------------- Read RTT and look for desired response --------------
    terminal_bytes=""
    status = False
    for i in range(1000):  # 10 second timeout
        terminal_bytes = terminal_bytes + "".join(map(chr, jlink.rtt_read(0, 1024)))

        #- The last line from the shell should contain the command prompt "rtt:~$" and end with a space " "
        #- The second last line should contain no prompt but contain other characters
        lines = re.split("\r\n", terminal_bytes)

        #Test and Wait for correct RTT response 
        status = False
        if len(lines) > 2:                                               # Nr of lines is higher than 2
            if (lines[-1].find('rtt:~$') != -1):                         # Last line contains a prompt
                if (lines[-2].find("rtt:~$") == -1):                     # Second last has no prompt
                    if (re.search('[a-zA-Z]', lines[-2]) is not None):   # Second last Contains letters
                        status = True
        if status:
            # We received a response
            response = lines[-2]
            log.debug("Rtt shell response when prompt found:%s",terminal_bytes)
            
            # Test if we received the correct response
            if terminal_bytes.find(desiredResponse) != -1:
                log.info("RTT Response: \"%s\" Pass!", response)
                status = True
            else:
                log.error("RTT Response: \"%s\" fail!", response)
                status = False     
            break
        else:
            time.sleep(0.01)

    return status

def flashHex(jlink,hexFile,log):
    log.info("Erasing flash...")
    jlink.erase()

    log.info("Flashing file %s...",hexFile)
    jlink.flash_file(hexFile,0)

    log.info("Reset device...\n")
    jlink.reset(10,False)


def getJLinkSerials(jlink):
    ConnectInfo = jlink.connected_emulators() #returns a list if JLinkConnectInfo objects
    serialNumbers = [o.__getattribute__("SerialNumber") for o in ConnectInfo] # Get the attribute SerialNumber from the objects
    return serialNumbers


def FLasAndConfig(serial_number, hexFile): #, log):
    log=setupLogger(serial_number)
    
    log.info("connecting to JLink...")
    jlink = pylink.JLink()
    jlink.disable_dialog_boxes()                    # Try to quiet the popups
    jlink.open(serial_number)
    
    log.info("connecting to device: %s..." % target_device)
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.connect(target_device)

    # #----- Erase and flash hex file --------------
    flashHex(jlink,hexFile,log)
    # # ---- Connect to RTT shell --- 
    log.info("Starting RTT...")
    jlink.rtt_start()

    #---- Fill rtc buffer with junk to se iff we are able to empty it
    jlink.rtt_write(0, list(bytearray("help","utf-8") + b"\x0A\x00"))
    time.sleep(0.5)

    #---- Send some commands over RTT to test it
    rtt_command(jlink, "modem start",log)
    rtt_command(jlink, "modem stop",log)
    rtt_command(jlink, "modem set psk ghnml",log)
    rtt_command(jlink, "modem set psk fgggg",log)
    rtt_command(jlink, "modem set psk bfbfb",log)
    rtt_command(jlink, "modem set psk bfbbb",log)
    rtt_command(jlink, "modem set psk grggg",log)
    rtt_command(jlink, "modem set psk ghwwh",log)


    rtt_command(jlink, "modem get psk",log)
    rtt_command(jlink, "modem set psk sderww",log)
    rtt_command(jlink, "modem get psk",log)


    jlink.rtt_stop()
    jlink.close()
    log.info("Time at exit")


if __name__ == "__main__":
    
    serial_number=sys.argv[1]
    hexFile=str(sys.argv[2])
    FLasAndConfig(serial_number, hexFile)
