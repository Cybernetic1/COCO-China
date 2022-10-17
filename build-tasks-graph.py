from neo4j import GraphDatabase
import re

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "l0wsecurity"))

"""
def create_word(tx, chars):
	tx.run("CREATE (a :Word {chars: $chars})",
		chars=chars)

def create_char(tx, char):
	tx.run("CREATE (a :Char) WHERE a.char = $char",
		char=char)

def create_rel(tx, char, chars):
	# "MERGE (b :Word {chars: $chars}) "
	tx.run( "MERGE (a :Char {char: $char}) "
			"MERGE (b :Word {chars: $chars}) "
			"MERGE (a)-[:In]->(b)",
			char=char, chars=chars)
"""

def create_node(tx, name):
	tx.run( "CREATE (a :Node {name: $name})",
			name=name)

with driver.session() as session:
	session.execute_write(create_node, "root")
	session.execute_write(create_node, "商业计划书")
	session.execute_write(create_node, "技术白皮书")
	session.execute_write(create_node, "网站")
	session.execute_write(create_node, "Git 界面")
	session.execute_write(create_node, "Neo4j 界面")
	session.execute_write(create_node, "聊天室 界面")
	session.execute_write(create_node, "DAO 界面")

	# Link all nodes as children of 'root'
	session.execute_write( lambda tx: tx.run(
		"MATCH (a:Node), (b:Node) WHERE b.name = 'root'"
		"CREATE (a)-[r:SubTask]->(b)"
		) )

	# Remove self-loop
	session.execute_write( lambda tx: tx.run(
		"MATCH (n:Node)-[r]->(n) WHERE n.name = 'root' DELETE r"
		) )

driver.close()

exit(0)
