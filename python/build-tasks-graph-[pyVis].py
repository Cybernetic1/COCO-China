# make a new neworkx network
import networkx as nx
G=nx.DiGraph()

nodes = ["Root", "商业计划书", "技术白皮书", "网站", "Git 界面", "Neo4j 界面",
	"聊天室 界面", "DAO 界面"]

# add nodes and edges
for n in nodes:
	G.add_node(n, shape='box')

for n in nodes[1:]:
	G.add_edge(n, 'Root')

from pyvis.network import Network

vis = Network(height='700px', width='100%', directed=True, bgcolor='#C9F9FF')

# populates the nodes and edges data structures
vis.from_nx(G)

html = vis.generate_html()
with open("pyVis.html", "w+") as out:
	out.write(html)

print("Created Project Graph.")
exit(0)
