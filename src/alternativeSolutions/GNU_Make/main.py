#!/usr/bin/env python3


import subprocess

#this is the Main script for setting up the system to configure all boards for flashing
print("setting up panel for paralell programming.")
# Execute flashing of all boards in the panel
print("Starting paralell programming: $(date)")

subprocess.run(["make", "-j10", "-k", "flash_all"])


print("Finished paralell programming:")