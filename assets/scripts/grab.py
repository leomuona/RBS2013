#!/usr/bin/env python

# Grab n throw python script for Blender game engine.
#
# eh.. should work somehow like dis:
#
# We have camera, shoot a ray from the middle point.
# If the ray hits some dynamic object, and its distance is
# small enough, set us, the camera, as the parent of the object.
# Then the object should follow all our moves, and simulate 'grabbing'

# the hard part is, how to do this with the API provided by BGE,
# as it is completely new for me.

# here are something i used for reference:
# http://www.blender.org/documentation/blender_python_api_2_69_0/
# http://www.cgmasters.net/free-tutorials/python-scripting/
# http://www.blender.org/documentation/blender_python_api_2_69_0/bge.types.KX_GameObject.html?highlight=ray#bge.types.KX_GameObject.rayCast

# and now after being done, twas suprisingly easy.
# of course, parenting didn't work, caused all kinds of funny bugs.
# also, it is still quite buggy, there is no collision with static objects
# (you can grab and push objects beyond floor and walls).
# but the basic idea is there
# Usage requires ray and mouse sensors, ray should be pulsed and freq 0

import math
from bge import logic
from mathutils import Matrix, Vector

class GNTCore:
	def __init__(self, object):
		self.own = object
		self.cont = None
		self.hits = 0

		# prev ray dir and range, used for calculating forces.
		# also player movement is followed like this.
		self.prevRayDir = None
		self.prevRayRange = None
		self.prevPlayerPos = None
		self.target = None

		if isCont(object):
			self.cont = object
			self.own = object.owner

		# have we grabbed some object
		self.grabbed = False

		self.raySen = None
		self.mouseSen = None

		objects = [self.own]

		for obj in objects:
			for s in obj.sensors:
				if str(s.__class__) == "<class 'KX_RaySensor'>":
					self.raySen = s
				elif str(s.__class__) == "<class 'SCA_MouseSensor'>":
					self.mouseSen = s

		if self.raySen == None:
			print("ERROR: No RaySensor set")
		if self.mouseSen == None:
			print("ERROR: No MouseSensor set")

		# setup sensor:
		if self.raySen != None:
			self.raySen.range = 5
			self.raySen.useXRay = False
			self.raySen.axis = 5 # KX_RAY_AXIS_NEG_Z

	def module(self):
		self.main()

	def main(self):
		if self.raySen == None or self.mouseSen == None:
			return

		if self.grabbed:
			self.mainGrabbed()
		else:
			self.initGrab()

	def initGrab(self):
		if self.raySen.positive and self.mouseSen.positive:
			#  don't grab massless objects... those are STATIC
			if self.raySen.hitObject.mass > 0:
				self.target = self.raySen.hitObject
				self.grabbed = True
				self.localHitPos = self.target.worldPosition - Vector(self.raySen.hitPosition)
				self.distance = (self.own.worldPosition - Vector(self.raySen.hitPosition)).length
				# suspend the dynamics during the translations
				self.target.suspendDynamics()

	def mainGrabbed(self):
		if self.mouseSen.positive and self.raySen.hitObject == self.target:
			hitRay = Vector([x * self.distance for x in self.raySen.rayDirection])
			self.target.worldPosition = self.own.worldPosition.copy() + hitRay + self.localHitPos
		else:
			self.prevRayDir = None
			self.prevRayRange = None
			self.prevPlayerPos = None
			self.grabbed = False
			if self.target != None:
				self.target.restoreDynamics()
			self.target = None


def isCont(object):
	if str(object.__class__) == "<class 'SCA_PythonController'>":
		return True
	return False

# Module Execution entry point
def main():
	cont = logic.getCurrentController()
	own = cont.owner

	if 'gnt.core' not in own:
		own['gnt.core'] = GNTCore(cont)
	else:
		own['gnt.core'].module()

# Non-Module Execution entry point (Script)
if logic.getCurrentController().mode == 0:
	main()