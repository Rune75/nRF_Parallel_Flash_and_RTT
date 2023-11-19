# nRF devices parallel programming and RTT shell configuration
Example code in Python intended as a proof of concept for parallel flashing and RTT shell configuration of nRF devices from Nordic Semiconductor. The examples should also work the same for all setups using SEGGER JLink and RTT shell for device interface. The provided examples runs both flashing and RTT communication in parallel processes. Logging is done into separate files for each of the connected JLink programmers.

The flashing stage will upload a minimal RTT shell application to the connected device. the shell application wil not do anything else than presenting a few function interfaces with various simulated responses in the RTT shell. The shell application hex files is currently compiled for the nRF52840dk board. To build the firmware for another device the source code can be found here: https://github.com/Rune75/nRF_Dummy_RTT_shell

### Dependencies 
pylink  
SEGGER JLink

### Usage connect the
Connect nRF52840 devices to the computer trough multiple JLink USB adapters.
#### Execute the Python example  
cd src  
./main.py

Combined log goes to stdOut, and device individual logs will go to separate files per JLink serial number.