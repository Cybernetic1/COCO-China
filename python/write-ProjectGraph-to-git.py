# Output Project Graph to Git repo
# ================================
# Each node = one directory
# Organized by distance from "Root"

import os

with open("ProjectGraph.json", "r") as infile:
	json_str = infile.read()
net = json.loads(json_str)
print("Net = ", net)

# Algorithm:
# 1. start from Root
# 2. find all nodes pointing to root,
# 3.     create dirs for these nodes
# 4. find all nodes pointing to these nodes, minus those already dealt with
# 5.     create dirs for these nodes
# 6. and so on...

frontier = ['Root']
create_dir_level(0)
create_dir_node("Root")

# If test-run, only print results
def mkdir(d):
	print("mkdir " + d)
	#os.mkdir(d)	# comment this out, you
	return

# Strip filename of any unwanted chars
safe_chars = set(map(lambda x: ord(x), '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-_ .'))

def clean_name(name):
    return ''.join(map(lambda ch: chr(ch) if ch in safe_chars else '%%%02x' % ch, name.encode('utf-8')))

clean = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", dirty)

# find all nodes connected to frontier nodes
def create_dir_level(l):
	mkdir("level" + str(l))
	for f in frontier:
		g = find_connected(f)
		for node in g:
			os.mkdir(node)

def create_dir_node(n):
	mkdir("n")
	with open("nodes_n_edges.json", "w+") as outfile:
		json_str = infile.read()
	
