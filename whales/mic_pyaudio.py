CAN = False
try:
	import pyaudio
	CAN = True
except Exception, e:
	print (e)
