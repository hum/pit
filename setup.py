#!/usr/bin/env python3

from setuptools import setup

setup(
	name = 'pit',
	version = '0.0.1',
	packages = ['pit'],
	entry_points = {
		'console_scripts': [
			'pit = pit.cli:main'
		]
	}
)
