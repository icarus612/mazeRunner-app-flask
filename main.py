from flask import Flask, render_template, url_for, session, request, redirect
import requests
import os
from maze import Maze
from runner import Runner

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/built', methods=['GET', 'POST'])
def index():
	layout = session.get(request.args.get('maze'))
	solved = session.get(request.args.get('solved'))
	print(layout, solved)
	return render_template('index.html', layout=layout, solved=solved)

@app.route('/make_maze', methods=['POST'])
def make_maze():
	height = int(request.form['height'])
	width = int(request.form['width'])
	maze_type = request.form['type']
	maze = Maze(build=[(width, height), maze_type])
	runner = Runner(maze)
	runner.make_node_paths()
	session[f"{maze}"] = maze.view_layout()
	complete = "Yes" if runner.completed else "No"
	print(f"Is maze possible? {complete}")
	if runner.completed:	
		runner.build_path()
	session[f"{runner}"] = runner.view_completed()
	return redirect(url_for('index', maze=maze, solved=runner))


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000)) 
	app.secret_key = os.urandom(24).hex()
	app.run(debug=True, port=port)