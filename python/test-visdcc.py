# TO-DO:

# DONE:
# * radio buttons for Done (pink) vs In-progress
# * link nodes
# * color node bug (fixed: set global variable)
# * fill task_name when select node

import dash
import visdcc
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
# from dash import Dash, Input, Output, State, dcc, html, callback_context
import json

app = dash.Dash(__name__)

# --bg: #C9F9FF;

styles = {
	'pre': {
		'width': '60px',
		'border': 'thin solid black',
		'overflowX': 'scroll'
	}
}

app.layout = html.Div([
	visdcc.Network(id = 'net',
		options = dict(height= '600px', width= '100%'),
		style = {
		'background-color': '#C9F9FF',
		'nodes': {
		'font': {
			# required: enables displaying <b>text</b> in the label as bold text
			'multi': 'html',
			# optional: use this if you want to specify the font of bold text
			# bold: '16px arial black'
			}
		}}),
	html.Label("Task name", id='task_nameLabel'),
	html.Br(),
	dcc.Input(id = 'task_name',
		placeholder = 'Task name:',
		type = 'text',
		style = {'display':'inline-block'},
		value = '' ),
	dcc.RadioItems(id = 'Status',
		options=[
			{'label': 'In Progress', 'value': None},
			{'label': 'Done', 'value': 'pink'} ],
		style = {'display':'inline-block'},
		value = None),
	html.Label("  [Color = ●]", id='taskStatus', style={'color':'red'}),
	html.Br(),html.Br(),
	html.Button('Add node', id='addNode'),
	html.Button('Delete node', id='delNode'),
	html.Button('Link nodes', id='linkNodes'),
	html.Button('Renew node details', id='renewNode'),
	html.P(children = "Selected Nodes: ②=none ①=none", id='selectedNode'),
	html.Br(),
	html.Button('Save graph', id='saveGraph'),
	html.Button('Load graph', id='loadGraph'),
])

selected_node_1 = None
selected_node_2 = None

task_name = ""
task_status = None

def ordinal(a, b):
	"""
	# A function to convert 2 numbers ('to' and 'from') into 1 number
	# But it's not very meaningful to save just a few bytes
	# So we won't use it.
	oct_a = "{0:o}".format(a)
	oct_b = "{0:o}".format(b)
	c = ""
	for i in range(max(len(oct_a), len(oct_b))):
		hex_c = "0123456789ABCDEF"[int(oct_a[i]) + int(oct_b[i])]
		c = hex_c + c
	return int(c, 16)
	"""
	return str(a)+'-'+str(b)

# ===== Create initial Project Graph =====

nodes = ["Root", "商业计划书", "技术白皮书", "网站", "Git 界面", "Neo4j 界面",
	"聊天室 界面", "DAO 界面"]

net = { 'nodes': [], 'edges': []}
node_index = 0
for n in nodes:
	net['nodes'].append({'id': node_index, 'label': n, 'shape': 'box'})
	node_index += 1

# decorate Root node
net['nodes'][0]['color'] = 'cyan'
# net['nodes'][0]['style'] = {'font': { 'size': 24, 'color': 'white' }}

node_index = 1
for n in nodes[1:]:
	net['edges'].append({'id': ordinal(node_index, 0), 'from': node_index, 'to': 0, 'arrows': 'to'})
	node_index += 1

# ===== Process callback events =====

@app.callback(								# select Node in graph
	Output('selectedNode', 'children'),
	Input('net', 'selection'))
def clicked_node(selected):
	global selected_node_1, selected_node_2
	print("selected =", selected)
	if selected is not None and len(selected['nodes']) > 0:
		newNode = selected['nodes'][0]
		if selected_node_1 != newNode:
			selected_node_2 = selected_node_1
			selected_node_1 = newNode
	name_1 = next((n['label'] for n in net['nodes'] if n["id"] == selected_node_1), "none")
	name_2 = next((n['label'] for n in net['nodes'] if n["id"] == selected_node_2), "none")
	return "Selected Nodes: ②=[" + name_2 + "] ①=[" + name_1 + "]"

@app.callback(								# Task Name changed by clicking node
	Output(component_id='task_name', component_property='value'),
	Input('net', 'selection'))
def myfun(selected):
	if selected is not None and len(selected['nodes']) > 0:
		s = selected['nodes'][0]
		val = next((n['label'] for n in net['nodes'] if n["id"] == s), None)
		return val
	return None

@app.callback(								# typing in Task Name
	Output(component_id='task_nameLabel', component_property='children'),
	Input(component_id='task_name', component_property='value'),
	)
def myfun(val):
	global task_name
	task_name = val
	return "Task name = " + (val if val is not None else "")

@app.callback(								# Task status = Done / inProgress
    Output('taskStatus', 'style'),
    Input('Status', 'value'))
def myfun(val):
	global task_status
	print("Status =", val)
	task_status = val
	if val == 'pink':
		return {'color':'red'}
	else:
		return {'color':'blue'}

@app.callback(								# Click various buttons
	Output('net', 'data'),
	dash.dependencies.Input('addNode', 'n_clicks'),
	dash.dependencies.Input('delNode', 'n_clicks'),
	dash.dependencies.Input('linkNodes', 'n_clicks'),
	dash.dependencies.Input('renewNode', 'n_clicks'),
	dash.dependencies.Input('saveGraph', 'n_clicks'),
	dash.dependencies.Input('loadGraph', 'n_clicks')
	)
def myfun(btn1, btn2, btn3, btn4, btn5, btn6):
	global net, node_index, task_name, task_status, selected_node_1, selected_node_2
	print("node_index =", node_index)
	print("task_name =", task_name)
	print("selected_node_1 =", selected_node_1)
	# print("triggered = ", callback_context.triggered)
	button_id = callback_context.triggered[0]['prop_id']
	print(button_id + " clicked")

	if button_id[:7] == 'addNode':
		net['nodes'].append({'id': node_index, 'label': task_name, 'shape': 'box'})
		net['edges'].append({'id': ordinal(node_index, selected_node_1),
			'from': node_index, 'to': selected_node_1, 'arrows': 'to'})
		node_index += 1
		return net

	if button_id[:7] == 'delNode':
		print("# nodes =", len(net['nodes']))
		for n in net['nodes']:
			print("matching:", n)
			if n['id'] == selected_node_1:
				net['nodes'].remove(n)
		# Don't forget to delete all edges to OR from this node!
		collection = []
		for e in net['edges']:
			print("matching:", e)
			if e['to'] == selected_node_1 or \
			   e['from'] == selected_node_1:
				print("Will delete edge:", e)
				collection.append(e)
		for e in collection:
			net['edges'].remove(e)
		# print("result =", net)
		return net

	if button_id[:9] == 'linkNodes':
		net['edges'].append({'id': ordinal(selected_node_2, selected_node_1),
			'from': selected_node_2, 'to': selected_node_1, 'arrows': 'to'})
		return net

	if button_id[:9] == 'renewNode':
		for n in net['nodes']:
			if n['id'] == selected_node_1:
				if task_name is not None:
					n['label'] = task_name
				n['color'] = task_status
				# etc ...
		return net

	if button_id[:9] == 'saveGraph':
		# json_str = json.dumps(net, indent=2)
		json_str = json.dumps(net, separators=(',', ':'))
		print("To save: ", json_str)
		with open("ProjectGraph.json", "w+") as outfile:
			outfile.write(json_str)
		return net

	if button_id[:9] == 'loadGraph':
		with open("ProjectGraph.json", "r") as infile:
			json_str = infile.read()
		net = json.loads(json_str)
		print("Net = ", net)
		return net

	return net

if __name__ == '__main__':
	app.run_server()
