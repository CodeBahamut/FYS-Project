from BrickPi import * #import BrickPi.py file to use BrickPi operations
import threading
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import time

c=0
#Initialize TOrnado to use 'GET' and load index.html
class MainHandler(tornado.web.RequestHandler):
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("index.html").generate())

#Code for handling the data sent from the webpage
class WSHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print 'connection opened...'
	def check_origin(self,origin):
		return True
	def on_message(self, message):      # receives the data from the webpage and is stored in the variable message
		global c
		print 'received:', message        # prints the revived from the webpage
		if message == "u":                # checks for the received data and assigns different values to c which controls the movement of robot.
		  c = "8";
		if message == "d":
		  c = "2"
		if message == "l":
		  c = "6"
		if message == "r":
		  c = "4"
		if message == "b":
		  c = "5"
		print c
		if c == '8' :
		  print "Running Forward"
		  BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
		  BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorD (-255 to 255)
		elif c == '2' :
		  print "Running Reverse"
		  BrickPi.MotorSpeed[PORT_A] = -200
		  BrickPi.MotorSpeed[PORT_D] = -200
		elif c == '4' :
		  print "Turning Right"
		  BrickPi.MotorSpeed[PORT_A] = 200
		  BrickPi.MotorSpeed[PORT_D] = 0
		elif c == '6' :
		  print "Turning Left"
		  BrickPi.MotorSpeed[PORT_A] = 0
		  BrickPi.MotorSpeed[PORT_D] = 200
		elif c == '5' :
		  print "Stopped"
		  BrickPi.MotorSpeed[PORT_A] = 0
		  BrickPi.MotorSpeed[PORT_D] = 0
		BrickPiUpdateValues();                # BrickPi updates the values for the motors
		print "Values Updated"
	def on_close(self):
		print 'connection closed...'

application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/', MainHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Ready"
        while running:
            BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
            time.sleep(.2)              # sleep for 200 ms

if __name__ == "__main__":
	BrickPiSetup()  						# setup the serial port for communication
	BrickPi.MotorEnable[PORT_A] = 1 		#Enable the Motor A
	BrickPi.MotorEnable[PORT_D] = 1 		#Enable the Motor D
	BrickPiSetupSensors()   				#Send the properties of sensors to BrickPi
	running = True
	thread1 = myThread(1, "Thread-1", 1)
	thread1.setDaemon(True)
	thread1.start()
	application.listen(9093)          	#starts the websockets connection
	tornado.ioloop.IOLoop.instance().start()