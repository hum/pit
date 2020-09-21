## manages the .pit directiory
import os
import hashlib

PIT_DIR = '.pit'

def init():
	os.makedirs(PIT_DIR)
	os.makedirs(f'{PIT_DIR}/objects')

def hash_object(data):
	old = hashlib.sha1(data).hexdigest()
	
	with open(f'{PIT_DIR}/objects/{oid}', 'wb') as out:
		out.write(data)
	
	return oid

def get_file(oid):
	with open(f'{PIT_DIR}/objects/{oid}', 'rb') as f:
		return f.read()
