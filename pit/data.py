## manages the .pit directiory

import os

PIT_DIR = '.pit'

def init():
	os.makedirs(PIT_DIR)
