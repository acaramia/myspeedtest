from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from flask import Flask, render_template, send_file, make_response, request

app = Flask(__name__)

from db.db_class import mydb

# main route
@app.route("/")
def index():
	db = mydb()
	rows = db.getData()
	row=rows[0]
	print(row)
	mbit = 1000000.0
	time = row['sqltime']
	download = row['download']/mbit
	upload = row['upload']/mbit
	ping = row['ping']
	templateData = {
		'time': time,
		'download': download,
		'upload': upload,
		'ping' : ping
	}
	return render_template('index.html', **templateData)

@app.route('/plot/downloads')
def plot_downloads():
	db = mydb()
	times,downloads, uploads,pings = db.getHistData()
	ys = downloads
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("downloads Mbit/s")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(len(ys))
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/pings')
def plot_pings():
	db = mydb()
	times,downloads, uploads,pings = db.getHistData()
	ys = pings
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("pings ms")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(len(ys))
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/uploads')
def plot_uploads():
	db = mydb()
	times,downloads, uploads,pings = db.getHistData()
	ys = uploads
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("uploads Mbit/s")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(len(ys))
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=False)