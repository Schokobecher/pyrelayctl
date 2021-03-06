#!/usr/bin/env python3
#
# Copyright (c) 2016, Heinrich Schuchardt <xypron.glpk@gmx.de>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#	notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#	notice, this list of conditions and the following disclaimer in the
#	documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import getopt
import relayctl
import sys

def checkport(dev, p): 
	""" 
	Checks if port p exists on the device.

	@param dev device
	@param p port
	@return port exists
	"""
	pmin = relayctl.getminport(dev)
	pmax = relayctl.getmaxport(dev)
	if p < pmin or p > pmax:
		print("Device {} only has ports {}..{}".format(
			relayctl.getid(dev), pmin, pmax))
		return False
	return True

def list(devices):
	"""
	List all devices.

	@param devices list of devices
	"""

	print("Available devices");

	for dev in devices:
		print('device {}'.format(devices.index(dev)), end=", ")
		# Print device id.
		print('id {}'.format(relayctl.getid(dev)))

def main():
	# Find our devices
	devices = relayctl.connect()

	# Were they found?
	if len(devices) == 0:
		print('No device found')
		sys.exit(1)
	
	# if there is only one device, use it as default.
	if len(devices) == 1:
		dev = devices[0]
	else:
		dev = None

	# Define command line options.
	try:
		opts, args = getopt.getopt(sys.argv[1:], "D:d:f:ghko:st:")
	except getopt.GetoptError as err:
		print(str(err))
		usage()
		sys.exit(2)

	if len(opts) == 0:
		usage()
		print()
		list(devices)

	# Handle command line.
	for o, a in opts:
		if o == "-D":
			dev = None
			for d in devices:
				if relayctl.getid(d) == a:
					dev = d
					break
			if dev == None:
				print("device with id {} not found".format(a))
				break
		elif o == "-d":
			d = int(a)
			if d < 0 or d >= len(devices):
				print("unknown device {}".format(d))
				break
			dev = devices[d];
		elif o == "-f":
			p = int(a)
			if not checkport(dev, p):
				break
			relayctl.switchoff(dev, p)
			status(dev)
		elif o == "-g":
			status(dev)
		elif o == "-h":
			usage()
			print()
		elif o == "-k":
			relayctl.disable(dev)
		elif o == "-o":
			p = int(a)
			if not checkport(dev, p):
				break
			relayctl.switchon(dev, p)
			status(dev)
		elif o == "-s":
			list(devices)
		elif o == "-t":
			p = int(a)
			if not checkport(dev, p):
				break
			if relayctl.getstatus(dev, p) == 0:
				relayctl.switchon(dev, p)
			else:
				relayctl.switchoff(dev, p)
			status(dev)
		else:
			break

	# Workaround for bug in old version of usb library.
	devices = None

def status(dev):
	"""
	Outputs the status of a device.

	@param dev device
	"""

	# Print device id.
	print('id {}'.format(relayctl.getid(dev)))
	# Print status of all outlets.
	for i in range(relayctl.getminport(dev),
		       1 + relayctl.getmaxport(dev)):
		print('\tstatus[{}] = {}'.format(i,
		      relayctl.getstatus(dev, i)))

def usage():
	"""
	Outputs the online help.
	"""

	print( "Usage: relctl.py [OPTIONS]")
	print( "Switches FTDI relay boards")
	print()
	print( "  -D ID	id of device to be controlled")
	print( "  -d DEVICE     index of device to be controlled")
	print( "  -f OUTLET     switch outlet off")
	print( "  -g            get status")
	print( "  -h            print this help")
	print( "  -k            attach kernel driver")
	print( "  -o OUTLET     switch outlet on")
	print( "  -s            list available devices")
	print( "  -t OUTLET     toggle outlet")

if __name__ == "__main__":
	main()
