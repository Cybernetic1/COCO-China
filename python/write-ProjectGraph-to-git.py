# Output Project Graph to Git repo
# ================================
# Each node = one directory
# Organized by distance from "Root"

import os
import json
import re

with open("ProjectGraph.json", "r") as infile:
	json_str = infile.read()
net = json.loads(json_str)
# print("Net = ", net)

# If test-run, only print results
def mkdir(d):
	print("mkdir " + d)
	#os.mkdir(d)	# comment this out, you
	return

# Clean filename of any unwanted chars, allowing Chinese chars etc to remain
def clean_name(name):
	return ''.join(
		map(lambda ch: '%%%02x' % ord(ch)
		if re.match(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", ch)
		else ch, name) )

# Inverse function of the above
# TO-DO:  need rigorous proof that the inverve holds
# May need to escape the symbol % via % --> %% to prevent ambiguity
def unclean_name(name):
	return

# print(clean_name("试吓先*.txt"))

# Create node #i
def create_dir_node(path, i):
	node = next(n for n in net['nodes'] if n["id"] == i)
	name = clean_name(node['label'])
	mkdir(path + name + '[' + str(i) + ']')
	"""
	with open("nodes_n_edges.py", "w+") as outfile:
		outfile.write(json_str)
	with open("details.py", "w+") as outfile:
		outfile.write(json_str)
	"""
	return

# Algorithm:
# 1. start from Root
# 2. find all nodes pointing to root,
# 3.     create dirs for these nodes
# 4. find all nodes pointing to these nodes, minus those already dealt with
# 5.     create dirs for these nodes
# 6. and so on...

processed = [0]		# nodes that have been processed
# blanket = subset of "processed" nodes whose children we need to process next
# frontier = children of "blanket", to be processed now and would become "blanket" next

# Find all nodes with edges TOWARDS nodes in blanket:
def find_connected(frontier):
	global processed
	print("frontier =", frontier)
	results = []
	for f in frontier:
		print("Find edges towards:", f)
		for e in net['edges']:
			if e["to"] == f:
				print("  found:", e['id'])
				newbie = e['from']
				if newbie not in processed and \
				   newbie not in frontier:
					results.append(newbie)
	print("new frontier =", results)
	return results

frontier = [0]
level = 0
while len(frontier) > 0:
	# Create new dir-level
	path = "level" + str(level) + '/'
	mkdir(path)
	for f in frontier:
		create_dir_node(path, f)
	level += 1

	results = find_connected(frontier)
	processed += results
	print ("processed =", processed)
	frontier = results
