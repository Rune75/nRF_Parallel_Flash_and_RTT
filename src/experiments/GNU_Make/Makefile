
# nRFJprog programmer handles
panel1_serial="683671125"
panel2_serial="683525490"
panel3_serial="xx5"
panel4_serial="xd6"

flasher=../../FlashAndprovision.py
FILE=../../nRF_hexFiles/rttShell840.hex

flash_all: panel1 panel2# panel3 panel4 panel5 panel6

panel%: 
	@$(flasher) $($(@)_serial) $(FILE)
