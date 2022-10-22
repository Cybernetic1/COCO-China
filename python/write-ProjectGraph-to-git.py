# Output Project Graph to Git repo
# ================================
# Each node = one directory
# Organized by distance from "Root"

import 

with open("ProjectGraph.json", "r") as infile:
	json_str = infile.read()
net = json.loads(json_str)
print("Net = ", net)

