#!/usr/bin/python
#coding: utf8
import sys
import gtk,pygtk,gnomeapplet,gobject
import recvReading

pygtk.require('2.0')

def applet_factory(applet, iid):   
	label = gtk.Label("reciving..")
	label.set_use_markup(True)
	applet.add(label)
	applet.show_all()
	gobject.timeout_add(5000,updateSensors,applet)
	updateSensors(applet)
	return True
def updateSensors(applet):
	sensorReadings = recvReading.recvReading()
	output = ""
	for name, val in sensorReadings.iteritems():
                if val[0] == 'Temp': 
                	output += name + ': <b>'+ val[1]+ " °C </b>"
	applet.get_child().set_label(output)
	return True

if __name__ == '__main__':   # testing for execution
	if len(sys.argv) > 1 and sys.argv[1] == '-d': # debugging
		mainWindow = gtk.Window()
		mainWindow.set_title('Applet window')
		mainWindow.connect('destroy', gtk.main_quit)
		applet = gnomeapplet.Applet()
		applet_factory(applet, None)
		applet.reparent(mainWindow)
		mainWindow.show_all()
		gtk.main()
		sys.exit()
	else:
		gnomeapplet.bonobo_factory('OAFIID:SensorApplet_Factory', 
                                 gnomeapplet.Applet.__gtype__, 
                                 'Sensor applet', '0.5', 
                                 applet_factory) 
