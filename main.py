from flask import Flask, render_template, url_for, session, request, redirect, make_response
import requests
import os
from maze import Maze
from runner import Runner

app = Flask(__name__)
app.secret_key = "monkeypenny"
		
def run_maze(maze):
	runner = Runner(maze)
	runner.make_node_paths()
	complete = "Yes" if runner.completed else "No"
	print(f"Is maze possible? {complete}")
	if runner.completed:	
		runner.build_path()
	return runner

def make_cookie(maze, runner):
	res = make_response(redirect(url_for('index', maze=maze, solved=runner)))
	res.set_cookie(f"{maze}", maze.view_layout(), max_age=60*60*1)
	res.set_cookie(f"{runner}", runner.view_completed(), max_age=60*60*1)
	return res

@app.route('/')
@app.route('/built')
def index():
	layout = request.cookies.get(request.args.get('maze'))
	solved = request.cookies.get(request.args.get('solved'))
	return render_template('index.html', layout=layout, solved=solved)

@app.route('/upload_maze', methods=['POST'])
def upload_maze():
	maze_file = request.files['maze_file']
	txt = maze_file.stream.read().decode("utf-8")
	if txt == '':
		return redirect(url_for('index', maze=None, solved=None))
	else:
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
		maze = Maze(m1, start, end, wall, space)
		runner = run_maze(maze)
		return make_cookie(maze, runner)


@app.route('/make_maze', methods=['POST'])
def make_maze():
	height = int(request.form['height'])
	width = int(request.form['width'])
	maze_type = request.form['type']
	maze = Maze(build=[(width, height), maze_type])
	runner = run_maze(maze)
	make_cookie(maze, runner)
	return make_cookie(maze, runner)


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000)) 
	app.run(debug=True, port=port)