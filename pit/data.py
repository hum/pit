## manages the .pit directiory
import os
import hashlib

PIT_DIR = '.pit'

def init():
	os.makedirs(PIT_DIR)
	os.makedirs(f'{PIT_DIR}/objects')

def hash_object(data, type_ = 'blob'):
	obj = type_.encode() + b'\x00' + data
	oid = hashlib.sha1(obj).hexdigest()
	
	with open(f'{PIT_DIR}/objects/{oid}', 'wb') as out:
		out.write(obj)
	return oid

def get_object(oid, expected = 'blob'):
	with open(f'{PIT_DIR}/objects/{oid}', 'rb') as f:
		obj = f.read()

	first_null = obj.index(b'\x00')
	type_ = obj[:first_null].decode()
	content = obj[first_null + 1:]

	if expected is not None:
		assert type_ == expected, f'Expected {expected}, got {type_}'
	
	return content

def get_HEAD():
  if os.path.isfile(f'{PIT_DIR}/HEAD'):
    with open(f'{PIT_DIR}/HEAD') as f:
      return f.read().strip()

def set_HEAD(oid):
  with open(f'{PIT_DIR}/HEAD', 'w') as f:
    f.write(oid)  

