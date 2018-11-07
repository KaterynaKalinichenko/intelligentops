
# This reads or writes something
import json


def read_file(file):
	with open(file, encoding='utf-8') as stream:
		return stream.read()


def write_json(json_dict, file):
	with open(file, mode='w', encoding='utf-8') as stream:
		return stream.write(json.dumps(json_dict, indent=2))
