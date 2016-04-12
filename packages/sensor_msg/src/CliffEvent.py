#!/usr/bin/env python
#coding=utf-8
""" 
this code is a util for cliffevent

Copyright (c) 2015 Xu Zhihao (Howe).  All rights reserved.

This program is free software; you can redistribute it and/or modify

This programm is tested on kuboki base turtlebot. 

"""
import rospy,serial
from sensor_msg.msg import Cliff_Event
import list_ports_linux

class cliff():
  
 def defination(self):
  self.event=Cliff_Event()
  self.pub = rospy.Publisher('/mobile_base/events/bumper', Cliff_Event, queue_size=1)
  self.serial2msg_dict={hex(01):'LEFT',hex(10):'RIGHT', 
                        hex(11):'FRONT',hex(00):'BACK'}
  
 def port_finder(self,trigger):
  ports = list(list_ports_linux.comports())
  for port in ports:
   if port[1]=='port_ID' or port[1]=='port_name':#根据具体情况定义
    trigger = True
    rospy.loginfo( 'rplidar connect on port: %s'%port[0])
    return [port,trigger]
   else:
    port=[]
  return[port,trigger]
  
 def __init__(self,trigger=False):
  rospy.loginfo( 'building node CliffEvent')
  rospy.init_node('CliffEvent', anonymous=False)
  rospy.loginfo( 'perparing for system parameters')
  self.defination()
  self.not_start=True
  rospy.loginfo( 'start connecting to port')
  port=self.port_finder(trigger)
  if 1:#for testing
  if self.port[1]:#
   self.port = serial.Serial("%s"%port[0][0],115200)
   self.port.flushInput()# discarding all flush input buffer contents
   rospy.loginfo('clear buffer done\n\n\n\n')
   while not rospy.is_shutdown():
    bytes=2 # read up to ten bytes (timeout)
    _str = self.port.read(bytes)
    #_str = hex(int(raw_input("\npls input bytes: ")))#for testing
    if self.serial2msg_dict[_str]=='LEFT':
     self.event.bumper=self.event.LEFT
     self.event.state=self.event.PRESSED
    if self.serial2msg_dict[_str]=='RIGHT':
     self.event.bumper=self.event.RIGHT
     self.event.state=self.event.PRESSED
    if self.serial2msg_dict[_str]=='FRONT':
     self.event.bumper=self.event.CENTER
     self.event.state=self.event.PRESSED
    if self.serial2msg_dict[_str]=='BACK':   
     self.event.bumper=self.event.BACK
     self.event.state=self.event.PRESSED
    if self.serial2msg_dict[_str]=='empty':  
     self.event.state=self.event.RELEASED
    print self.serial2msg_dict[_str]
    self.pub.publish(self.event)
    rospy.sleep(1)
    self.event.state=self.event.RELEASED
    self.pub.publish(self.event)
  else:
   rospy.loginfo('cannot find rplidar please connect rplidar on')
   pass 
  self.port.close()
  
  
if __name__ == "__main__":
 try:
  rospy.loginfo("initialization system")
  cliff()
  rospy.loginfo( "process done and quit")
 except rospy.ROSInterruptException:
  rospy.loginfo("unknown_detector node terminated.")

