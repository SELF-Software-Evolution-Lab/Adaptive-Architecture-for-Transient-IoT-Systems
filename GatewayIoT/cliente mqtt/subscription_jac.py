#
#	subscription.py
#
#	(c) 2017 by Andreas Kraft
#	License: BSD 3-Clause License. See the LICENSE file for further details.
#
#	This example shows how to susbcribe to resources and receive notifications.
#

from onem2mlib import *
import uuid, sys, time
import onem2mlib.constants as CON
import onem2mlib.notifications as NOT
sys.path.append('..')


# This is the callback function that is called for the notifications.
# The parameter is the changed resource
def callback(resource):
    if resource.type == CON.Type_ContentInstance:
        print(resource)       
    else:
        print(resource)

if __name__ == '__main__':

	# Setup the notification sub-system
	print('Setting up notifications...')
	#the ip of these notifications is your IP. this configures an IP server to receive OM2M notifications
	NOT.setupNotifications(callback, host='127.0.0.1', port=1400)

	# Create session
	session = Session('http://127.0.0.1:8080', 'admin:admin')

	# Get the <CSEBase> resource
	# cse = CSEBase(session, 'mn-cse')
	cse = CSEBase(session, 'in-cse')

	# create an <AE> resource
	aeName = 'park_rain2'
	# aeName = 'sensor_casa'
	ae = AE(cse, aeName)


	# create a <container> and add it to the <AE>
	# cnt = Container(ae,"Healthcheck")
	# cnt.subscribe()
	# print(cnt.resourceID)
	cnt2 = Container(ae, "DATA")
	cnt2.subscribe()


	# Change the <container> to trigger a notification for that resource
	cnt2.maxNrOfInstances = 10
	cnt2.updateInCSE()

	# Add a <contentInstance> to the <Container> to trigger a notification
#	cnt.addContent('Some value')

	# Give the cse a moment to process the notification before shutting down the notification
	# sub-system
	time.sleep(100)

	# Shutdown the notification sub-system (actually not really necessary)
	print('Shutting down notifications...')
	NOT.shutdownNotifications()

	# Cleanup
#	ae.deleteFromCSE()
