#!/usr/bin/python

from multiprocessing import Process
import os

class One (Process):
    def __init__(self,s):
	Process.__init__(self)
	self.size = s

    def repeat(self,out) :
	for i in range(self.size):
	    print("{0} - {1} / {2}".format(out,i,os.getpid()))

    def setOut(self,out) :
	self.out = out

    def run(self):
	self.repeat(self.out)

    @staticmethod
    def doit(s,out) :
	obj = One(s)
	obj.repeat(out)
	



p1 = Process(target=One.doit, args=(10,"one"))
p2 = Process(target=One.doit, args=(10,"two"))
p1.start()
p2.start()
p1.join()
p2.join()


a = One(100100)
b = One(100000)
c = One(100100)
d = One(100000)

a.setOut('three')
b.setOut('four')
c.setOut('five')
d.setOut('six')

a.start()
b.start()
c.start()
d.start()

a.join()
b.join()
c.join()
d.join()
