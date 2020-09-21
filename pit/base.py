from . import data
import os

def write_tree(directory = '.'):
	entries = []
	with os.scandir(directory) as dir_:
		for obj in dir_:
			full = f'{directory}/{obj.name}'

			if is_ignored(full):
				continue

			if obj.is_file(follow_symlinks = False):
				type_ = 'blob'

				with open(full, 'rb') as f:
					oid = data.hash_object(f.read())

			elif obj.is_dir(follow_symlinks = False):
				type_ = 'tree'
				oid = write_tree(full)
				entries.append((obj.name, oid, type_))

	tree = ''.join(f'{type_} {oid} {name}\n'
		for name, oid, type_ in sorted(entries)
	)

	return data.hash_object(tree.encode(), 'tree')

def is_ignored(path):
	return '.pit' in path.split('/') or '.git' in path.split('/') # we ignore .git as well so it doesn't cause a confusing output

def _iter_tree_entries(oid):
	if not oid:
		return

	tree = data.get_object(oid, 'tree')

	for obj in tree.decode().splitlines():
		type_, oid, name = obj.split(' ', 2)
		yield type_, oid, name

def get_tree(oid, base_path = ''):
	result = {}
	
	for type_, oid, name in _iter_tree_entries(oid):
		assert '/' not in name
		assert name not in ('..', '.')
		path = base_path + name

		if type_ == 'blob':
			result[path] = oid
		elif type_ == 'tree':
			result.update(get_tree(oid, f'{path}/'))
		else:
			assert False, f'Unknown object {type_}'

	return result

def _empty_current_directory():
	for root, _, filenames in os.walk('.'):
		for filename in filenames:
			path = os.path.relpath(f'{root}/{filename}')
			
			if is_ignored(path) or not os.path.isfile(path):
				continue

			os.remove(path)

def read_tree(tree_oid):
	_empty_current_directory()
	for path, oid in get_tree(tree_oid, base_path = './').items():
		os.makedirs(os.path.dirname(path), exist_ok = True)

		with open(path, 'wb') as f:
			f.write(data.get_object(oid))

def commit(message):
	commit = f'tree {write_tree()}\n'

	HEAD = data.get_HEAD()
	if HEAD:
		commit += f'parent {HEAD}'

	commit += '\n'
	commit += f'{message}\n'
  
	oid = data.hash_object(commit.encode(), 'commit')
	data.set_HEAD(oid)

	return oid
