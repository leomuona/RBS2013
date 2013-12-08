#!/usr/bin/env python

# import game engine modules
from bge import render
from bge import logic
# import stand alone modules
import bgl
import blf
import time

current_milli_time = lambda: int(round(time.time() * 1000))

def init():
	# create a new font object, use external ttf file
	font_path = logic.expandPath('//assets/fonts/LiberationMono-Regular.ttf')
	# store the font indice - to use later
	logic.font_id = blf.load(font_path)

	# set the font drawing routine to run every frame
	scene = logic.getCurrentScene()
	scene.post_draw = [write]

	logic.text_buffer = []

def show_das_points():
	''' expects that opengl mode is setup corrently '''
	width = render.getWindowWidth()
	height = render.getWindowHeight()

	text = 'Points: '+str(logic.getCurrentScene().objects["PinsRoof"]["points"])

	# BLF drawing routine
	font_id = logic.font_id
	#blf.position(font_id, width - 160, height - 24, 0) 
	blf.position(font_id, width * 0.2, height * 0.2, 0)
	blf.size(font_id, 24, 72)
	blf.draw(font_id, text)

def write():
	''' Uses text buffer for rendering stuff on screen
	
	Text buffer can be found from logic.text_buffer
	Each value in buffer is a hash, containing text, timeout and start_time
	start time is set by me, not you
	'''

	"""write on screen"""
	width = render.getWindowWidth()
	height = render.getWindowHeight()

	# OpenGL setup
	bgl.glMatrixMode(bgl.GL_PROJECTION)
	bgl.glLoadIdentity()
	bgl.gluOrtho2D(0, width, 0, height)
	bgl.glMatrixMode(bgl.GL_MODELVIEW)
	bgl.glLoadIdentity()

	show_das_points()

	if logic.text_buffer == None or len(logic.text_buffer) == 0:
		return
	
	text = ''
	
	# has the current value start time
	if 'start_time' in logic.text_buffer[0]:
		start_time = logic.text_buffer[0]['start_time']
		current_time = current_milli_time()
		timeout = logic.text_buffer[0]['timeout']
		if start_time + timeout < current_milli_time():
			logic.text_buffer.pop(0)
		else:
			text = logic.text_buffer[0]['text']
	else:
		logic.text_buffer[0]['start_time'] = current_milli_time()
		text = logic.text_buffer[0]['text']

	# BLF drawing routine
	font_id = logic.font_id
	blf.position(font_id, (width * 0.25), (height * 0.5), 0)
	blf.size(font_id, 24, 72)
	blf.draw(font_id, text)

init()

logic.text_buffer.append({'text' : 'Left-click to grab objects', 'timeout': 3000})
logic.text_buffer.append({'text' : 'Right-click to throw dem', 'timeout': 3000})