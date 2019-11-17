from flask import Flask, render_template, url_for, session, request, redirect
import requests
import os
from maze import Maze
from runner import Runner

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
@app.route('/built', methods=['GET', 'POST'])
def index():
	return render_template('index.html', layout=session.get(request.args.get('maze')), solved=session.get(request.args.get('solved')))

@app.route('/download/<file_name>')
def download(city, country, state=None):
	pass

@app.route('/solve_maze', methods=['POST'])
def solve_maze():
	try:
		city = request.form['city']
		state = request.form['state'] if request.form['state'] != "" else None
		country = request.form['country']
		return redirect(url_for('weather', city=city, country=country, state=state))
	except:
		return redirect(url_for('index'))

@app.route('/make_maze', methods=['POST'])
def make_maze():
	height = int(request.form['height'])
	width = int(request.form['width'])
	maze_type = request.form['type']
	maze = Maze(build=[(width, height), maze_type])
	runner = Runner(maze)
	runner.make_node_paths()
	complete = "Yes" if runner.completed else "No"
	print(f"Is maze possible? {complete}")
	session[f"{maze}"] = maze.view_layout()
	if runner.completed:	
		runner.build_path()
	session[f"{runner}"] = runner.view_completed()
	return redirect(url_for('index', maze=maze, solved=runner))

def open_and_build(file):
	with open(file) as m:
		txt = m.read()
		m1 = [list(i) for i in txt.split("\n")]
		flat = [y for x in m1 for y in x]
		s = set(txt)
		wall = txt[0][0]
		s.remove("\n")
		s.remove(wall)
		for i in s:
			if flat.count(i) == 1:
				pass
			else: 
				space = i
		s.remove(space)
		flat[:] = [x for x in flat if x != wall and x != space]
		start = flat[0]
		end = flat[1]
		return Maze(m1, start, end, wall, space)




port = int(os.environ.get('PORT', 5000)) 
app.secret_key = os.urandom(24).hex()
app.run(debug=True, port=port)